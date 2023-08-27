from django.urls import path

from . import views


urlpatterns = [
    path('send_sms', views.send_verification_sms),
    path('verify_sms_code', views.verify_sms_code),
]