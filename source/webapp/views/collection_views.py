from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from webapp.models import Coin, Country, Collection, Coin_in_Collection
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from webapp.forms import SearchForm, CoinForm, CollectionForm, CollectionCoinForm
from django.db.models import Q


class CollectionView(ListView):
    template_name = 'collections/collection_list.html'
    context_object_name = 'collections'
    paginate_by = 4
    paginate_orphans = 1

    def get_queryset(self, **kwargs):
        data = Collection.objects.filter(owner=self.request.user)
        # form = SearchForm(data=self.request.GET)
        # if form.is_valid():
        #     search = form.cleaned_data['search']
        #     if search:
        #         data = data.filter(Q(name__icontains=search))
        return data


class CollectionCoinCreateView(CreateView):
    template_name = 'collections/collection_coin_create.html'
    form_class = CollectionCoinForm
    model = Coin_in_Collection

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Coin, pk=pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        kwargs['pk'] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        coin = self.get_object()
        collection_coin = form.save(commit=False)
        collection_coin.owner = self.request.user
        country = get_object_or_404(Country, pk=coin.country.pk)
        collection_coin.country = country
        c = collection_coin.save()
        print(c)
        # form.save_m2m()  ## для сохранения связей многие-ко-многим
        return redirect('webapp:collection_coin_view', pk=collection_coin.pk)



class CollectionCoinDetailView(DetailView):
    model = Coin_in_Collection
    template_name = 'collections/collection_coin_detail.html'


class CollectionCreateView(CreateView):
    model = Collection
    template_name = 'collections/collection_create.html'
    form_class = CollectionForm

    def form_valid(self, form):
        collection = form.save(commit=False)
        collection.owner = self.request.user
        collection.save()
        # form.save_m2m()  ## для сохранения связей многие-ко-многим
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        print(next_url)
        if not next_url:
            next_url = self.request.POST.get('next')
            print(next_url)
        if not next_url:
            next_url = reverse('webapp:index')
        print(next_url)
        return next_url