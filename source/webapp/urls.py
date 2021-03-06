from django.urls import path, include
# from webapp.views import IndexView, CoinDetailView, CoinDeleteView, CoinCreateView, CollectionCreateView, CollectionCoinDetailView, CollectionCoinCreateView, CoinCategoryView, CountryCategoryView, CollectionView
from webapp.views import *
from django.conf.urls.static import static
from django.conf import settings
app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('country/<int:pk>/', include([
        path('', CountryCategoryView.as_view(), name='coin_country'),
    ])),
    path('coins/', include([
        path('<int:pk>/', include([
            path('', CoinDetailView.as_view(), name='coin_view'),
            path('delete/', CoinDeleteView.as_view(), name='coin_delete'),
            path('create/', CoinCreateView.as_view(), name='coin_create'),
        ])),
    ])),
    path('collection_coins/', include([
        path('<int:pk>/', include([
            path('', CollectionCoinDetailView.as_view(), name='collection_coin_view'),
            path('create/', CollectionCoinCreateView.as_view(), name='collection_coin_create'),
            path('delete/', CollectionCoinDeleteView.as_view(), name='collection_coin_delete'),
        ])),
    ])),
    path('offer/', include([
        path('<int:pk>/', include([
            path('create/', OfferCreateView.as_view(), name='offer_create'),
            path('delete/', OfferDeleteView.as_view(), name='offer_delete'),
            path('accept/', OfferAcceptView.as_view(), name='offer_accept'),
        ])),
    ])),
    path('collections/', include([
        path('', CollectionView.as_view(), name='collection_list'),
        path('create/', CollectionCreateView.as_view(), name='collection_create'),
        path('<int:pk>/', include([
            path('', CollectionDetailView.as_view(), name='collection_detail'),
            path('delete/', CollectionDeleteView.as_view(), name='collection_delete'),
        ])),
    ])),
    path('coins_category_list/<int:pk>/', CoinCategoryView.as_view(), name='coin_currency_nominal'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)