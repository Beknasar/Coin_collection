from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from webapp.models import Coin, Country, Currency, Nominal
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from webapp.forms import SearchForm, CoinForm
from django.db.models import Q


class IndexView(ListView):
    template_name = 'coins/index.html'
    context_object_name = 'countries'
    paginate_by = 4
    paginate_orphans = 1

    def get_queryset(self, **kwargs):
        data = Country.objects.all()
        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(name__icontains=search))
        return data


class CoinDetailView(DetailView):
    model = Coin
    template_name = 'coins/coin_detail.html'


class CoinDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'coins/coin_delete.html'
    model = Coin
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        return self.request.user.has_perm('webapp.delete_coin') or \
            self.get_object().owner == self.request.user


class CoinCreateView(LoginRequiredMixin, CreateView):
    template_name = 'coins/coin_create.html'
    form_class = CoinForm
    model = Coin

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        country = get_object_or_404(Country, pk=self.kwargs.get('pk'))
        kwargs['country'] = country
        return kwargs

    def form_valid(self, form):
        country = get_object_or_404(Country, pk=self.kwargs.get('pk'))
        coin = form.save(commit=False)
        currency = Currency.objects.get(pk=coin.currency.pk)
        Nominal.objects.get_or_create(nominal=coin.nominal, currency=currency)
        coin.owner = self.request.user
        coin.country = country
        coin.save()
        # form.save_m2m()  ## для сохранения связей многие-ко-многим
        return redirect('webapp:coin_view', pk=coin.pk)

    def get_success_url(self):
        return reverse('webapp:coin_view', kwargs={'pk': self.object.pk})


class CountryCategoryView(DetailView):
    model = Country
    template_name = 'coins/coin_categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        form = SearchForm(data=self.request.GET)
        data = Currency.objects.filter(country__pk=pk)
        context['form'] = form
        context['currencies'] = data.order_by('name')
        return context

    # ListView
    # def get_queryset(self, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     data = Currency.objects.filter(country__pk=pk)
    #     form = SearchForm(data=self.request.GET)
    #     if form.is_valid():
    #         search = form.cleaned_data['search']
    #         if search:
    #             data = Coin.objects.filter(Q(year_of_issue__icontains=search) | Q(currency__name__icontains=search))
    #     return data.order_by('currency',)


class CoinCategoryView(DetailView):
    model = Nominal
    template_name = "coins/coins_category_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        nom_nom = self.get_object()
        form = SearchForm(data=self.request.GET)
        data = Coin.objects.filter(Q(currency__pk=nom_nom.currency.pk) & Q(nominal=nom_nom.nominal))
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(year_of_issue__icontains=search))
            kwargs['search'] = search
        context['form'] = form
        context['coins'] = data.order_by('year_of_issue')
        return context