from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_confirm, reset_password, reset_password_success

app_name = UsersConfig.name

urlpatterns = [
    path('login', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register/confirm/<str:token>', email_confirm, name='confirm'),
    path('register', UserCreateView.as_view(), name='register'),
    path('register/reset-password-success', reset_password_success, name='reset-password-success'),
    path('register/reset-password', reset_password, name='reset-password'),
]
