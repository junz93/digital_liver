from django.urls import path

from . import views


urlpatterns = [
    path('alipay_callback', views.alipay_callback),
]