from django.urls import path

from . import views


urlpatterns = [
    path('info', views.get_subscription_info),
    path('get_alipay_url', views.get_alipay_payment_url),
    path('get_wechat_url', views.get_wechat_payment_url),
]