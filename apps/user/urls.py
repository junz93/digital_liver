from django.urls import path
from rest_framework.authtoken import views as auth_views

from . import views


urlpatterns = [
    path('auth_token', auth_views.obtain_auth_token),
    path('register', views.register),
    path('info', views.get_user_info),
    path('logout', views.log_out),
    path('delete', views.delete_user),
]