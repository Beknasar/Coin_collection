from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm, PasswordChangeForm
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from webapp.models import Coin, Country, Collection, Coin_in_Collection, Offer
from accounts.models import Profile
from webapp.forms import SearchForm


class RegisterView(CreateView):
    model = User
    template_name = 'user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


class UserListView(ListView):
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SearchForm(data=self.request.GET)
        user = User.objects.get(pk=self.request.user.pk)
        collection_coins = Coin_in_Collection.objects.filter(owner=user)
        offers = []
        for coin in collection_coins:
            if coin.offers:
                for offer in coin.offers.all():
                    offers.append(offer)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        kwargs['form'] = form
        kwargs['offers'] = offers
        kwargs['user'] = user
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = User.objects.all()
        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return data

    # def has_permission(self):
    #     return self.request.user.groups.filter(pk=2) or self.request.user.groups.filter(pk=3) or self.request.user.pk == 1


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        form.save()
        profile_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

        # if self.request.method == 'POST':
        #     form = ProfileChangeForm(instance=self.object, data= self.request.POST,
        #                              files=self.request.FILES)
        # else:
        #     form = ProfileChangeForm(instance=self.object)
        # return form


class UserPasswordChangeView(PermissionRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def has_permission(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_success_url(self):
        return reverse('accounts:login')
