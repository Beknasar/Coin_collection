from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from webapp.models import Coin, Country, Currency
from django.views.generic import ListView, DetailView, DeleteView, CreateView

from webapp.forms import SearchForm, CoinForm
from django.db.models import Q


class IndexView(ListView):
    template_name = 'coins/index.html'
    context_object_name = 'coins'
    paginate_by = 4
    paginate_orphans = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        kwargs['form'] = form
        kwargs['countries'] = Country.objects.all()
        kwargs['currencies'] = Currency.objects.all()

        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self, **kwargs):
        data = Coin.objects.all()
        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(country__name__icontains=search) | Q(year_of_issue__icontains=search) | Q(currency__name__icontains=search))

        return data.order_by('year_of_issue')


class CoinDetailView(DetailView):
    model = Coin
    template_name = 'coins/coin_view.html'


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

    def form_valid(self, form):
        coin = form.save(commit=False)
        coin.owner = self.request.user
        coin.save()
        # form.save_m2m()  ## для сохранения связей многие-ко-многим
        return redirect('webapp:coin_view', pk=coin.pk)

    def get_success_url(self):
        return reverse('webapp:coin_view', kwargs={'pk': self.object.pk})


class CategoryView(ListView):
    template_name = 'coins/coin_categories.html'
    context_object_name = 'coins'

    def get_queryset(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Coin.objects.filter(country__pk=pk).order_by('year_of_issue')