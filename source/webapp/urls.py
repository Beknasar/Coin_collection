from django.urls import path, include
from webapp.views import IndexView, CoinDetailView, CoinDeleteView, CoinCreateView, CategoryView
from django.conf.urls.static import static
from django.conf import settings
app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('coins/', include([
        path('<int:pk>/', include([
            path('', CoinDetailView.as_view(), name='coin_view'),
            path('delete/', CoinDeleteView.as_view(), name='coin_delete'),
        ])),
        path('create/', CoinCreateView.as_view(), name='coin_create'),
        path('category/<int:pk>/', CategoryView.as_view(), name='coin_category'),
    ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)