from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Subscription, SubscriptionOrder, SUBSCRIPTION_PRODUCTS
from services import payment
from utils.errors import create_error_response

import logging


@api_view(['GET'])
def get_subscription_info(request: Request):
    subscription = Subscription.get_unique(request.user)

    return Response({
        'subscription_status': Subscription.get_status(subscription),
        'subscription_expiry_time': Subscription.get_expiry_timestamp(subscription),
    })


@api_view(['POST'])
def get_alipay_payment_url(request: Request):
    params = request.data

    if 'product_id' not in params:
        logging.error('Bad Request')
        return create_error_response(status.HTTP_400_BAD_REQUEST, '参数缺失: product_id')

    subscription_product = SUBSCRIPTION_PRODUCTS.get(params['product_id'])
    if not subscription_product:
        return create_error_response(status.HTTP_400_BAD_REQUEST, '参数 product_id 无效')

    order_id = payment.generate_order_id(prefix=SubscriptionOrder.ORDER_ID_PREFIX)
    SubscriptionOrder.objects.create(
        order_id=order_id, 
        user=request.user, 
        product_id=params['product_id'],
        amount_str=subscription_product['price'],
        amount=subscription_product['price'],
    )

    url = payment.get_desktop_alipay_payment_url(
        order_id=order_id, 
        subject=subscription_product['order_product_name'], 
        total_amount=subscription_product['price'],
    )
    return Response({'url': url})


@api_view(['GET'])
def get_wechat_payment_url(request: Request):
    return Response(status=status.HTTP_404_NOT_FOUND)
