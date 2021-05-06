from webapp.models import Coin
from django.views.generic import ListView

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
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = Coin.objects.all()

        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            print(search)
            print(data)
            if search:
                data = data.filter(Q(country__name__icontains=search) | Q(year_of_issue__icontains=search))

        return data.order_by('-country')


