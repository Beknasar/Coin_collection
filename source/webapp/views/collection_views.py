from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from webapp.models import Coin, Country, Collection, Coin_in_Collection, Offer
from django.views.generic import ListView, DetailView, DeleteView, CreateView, View
from webapp.forms import CollectionForm, CollectionCoinForm, OfferForm



class CollectionView(ListView):
    template_name = 'collections/collection_list.html'
    context_object_name = 'collections'
    paginate_by = 4
    paginate_orphans = 1

    def get_queryset(self, **kwargs):
        data = Collection.objects.filter(owner=self.request.user)
        return data


class CollectionCoinDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'collections/coin/collection_coin_delete.html'
    model = Coin_in_Collection
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        return self.request.user.has_perm('webapp.delete_coin_in_collection') or \
               self.get_object().owner == self.request.user


class CollectionCoinCreateView(LoginRequiredMixin, CreateView):
    template_name = 'collections/coin/collection_coin_create.html'
    form_class = CollectionCoinForm
    model = Coin_in_Collection

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Coin, pk=pk)

    def get_initial(self):
        initial = {}
        coin = self.get_object()
        for key in 'picture', 'nominal', 'material', 'currency', 'weight', 'size', 'form', 'year_of_issue', 'year_of_issue_end', 'series', 'description':
            initial[key] = getattr(coin, key)
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs['instance'] = self.get_object()
        kwargs['coin'] = self.get_object()
        kwargs['pk'] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        coin = self.get_object()
        collection_coin = form.save(commit=False)
        # print(type(collection_coin))
        collection_coin.owner = self.request.user
        country = get_object_or_404(Country, pk=coin.country.pk)
        collection_coin.country = country

        c = collection_coin.save()
        print(type(c))
        # form.save_m2m()  ## для сохранения связей многие-ко-многим
        return redirect('webapp:collection_coin_view', pk=collection_coin.pk)


class CollectionCoinDetailView(DetailView):
    model = Coin_in_Collection
    template_name = 'collections/coin/collection_coin_detail.html'


class CollectionCreateView(LoginRequiredMixin, CreateView):
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


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'collections/collection_detail.html'


class CollectionDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'collections/collection_delete.html'
    model = Collection
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        return self.request.user.has_perm('webapp.delete_collection') or \
               self.get_object().owner == self.request.user


class OfferCreateView(CreateView):
    model = Offer
    form_class = OfferForm
    template_name = 'collections/coin/offer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coin'] = get_object_or_404(Coin_in_Collection, pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        offer = form.save(commit=False)
        amount = form.cleaned_data.get('amount', 1)
        offer.coin = get_object_or_404(Coin_in_Collection, pk=self.kwargs.get('pk'))
        offer.user = User.objects.get(pk=self.request.user.pk)
        if amount <= offer.coin.quantity:
            offer.save()
        else:
            offer.amount = offer.coin.quantity
            offer.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:index')


class OfferDeleteView(DeleteView):
    model = Offer
    success_url = reverse_lazy('accounts:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)

    # удаление без подтверждения
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class OfferAcceptView(View):
    def check_coin(self, coin):
        if coin.quantity == 0:
            coin.delete()
        coin.save()
        return coin

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        offer = get_object_or_404(Offer, pk=pk)
        # print(proposer)
        offer.coin.owner = offer.to_coin.owner
        offer.to_coin.owner = offer.user
        offer.to_coin.quantity -= offer.amount
        offer.coin.quantity -= 1
        self.check_coin(offer.to_coin)
        self.check_coin(offer.coin)
        offer.delete()
        return redirect("accounts:list")
