from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import RegisterView, UserDetailView, UserListView, UserChangeView, UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='create'),
    path('list/', UserListView.as_view(), name='list'),
    path('<int:pk>/', include([
        path('', UserDetailView.as_view(), name='detail'),
        path('update/', UserChangeView.as_view(), name='change'),
        path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
        ])),
]
