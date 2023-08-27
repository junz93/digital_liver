from django.db import models
from django.utils import timezone

from apps.user.models import User


class SubscriptionStatus:
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class Subscription(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    expiry_datetime = models.DateTimeField()
    created_datetime = models.DateTimeField(auto_now_add=True, editable=False)
    updated_datetime = models.DateTimeField(auto_now=True, editable=False)
    
    @classmethod
    def get_unique(cls, user: User):
        try:
            return cls.objects.get(user_id=user.id)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_status(cls, subscription):
        if not subscription:
            return SubscriptionStatus.INACTIVE
        return SubscriptionStatus.ACTIVE if subscription.expiry_datetime > timezone.now() else SubscriptionStatus.INACTIVE
    
    @classmethod
    def get_expiry_timestamp(cls, subscription):
        if not subscription:
            return None
        return int(subscription.expiry_datetime.timestamp())


class SubscriptionProductId:
    SP1 = 'SP1'
    SP2 = 'SP2'
    SP3 = 'SP3'


SUBSCRIPTION_PRODUCTS = {
    SubscriptionProductId.SP1: {
        'id': SubscriptionProductId.SP1,
        # 'price': '540.00',
        'price': '1.50',
        'time_months': 12,
        'order_product_name': '数字人直播 一年会员',
    },
    SubscriptionProductId.SP2: {
        'id': SubscriptionProductId.SP2,
        # 'price': '180.00',
        'price': '1.00',
        'time_months': 3,
        'order_product_name': '数字人直播 三个月会员',
    },
    SubscriptionProductId.SP3: {
        'id': SubscriptionProductId.SP3,
        # 'price': '90.00',
        'price': '0.50',
        'time_months': 1,
        'order_product_name': '数字人直播 一个月会员',
    },
}


class SubscriptionOrder(models.Model):
    PRODUCT_ID_CHOICES = [
        (SubscriptionProductId.SP1, '包年会员'),
        (SubscriptionProductId.SP2, '包季会员'),
        (SubscriptionProductId.SP3, '包月会员'),
    ]

    ORDER_ID_PREFIX = 'SUBS'

    order_id = models.CharField(max_length=64, primary_key=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product_id = models.CharField(max_length=8, choices=PRODUCT_ID_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    amount_str = models.CharField(max_length=15)
    created_datetime = models.DateTimeField(auto_now_add=True, editable=False)
    paid_datetime = models.DateTimeField(null=True, blank=True)
