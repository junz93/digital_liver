from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from apps.subscription.models import Subscription, SubscriptionOrder, SUBSCRIPTION_PRODUCTS
from apps.material.models import UserImage, UserEnvironment, Image, Environment, ImageOrder, EnvironmentOrder
from services import payment
from utils.renders import PlainTextRenderer

import logging

@api_view(['POST'])
@permission_classes([AllowAny])
@renderer_classes([PlainTextRenderer, BrowsableAPIRenderer])
def alipay_callback(request: Request):
    params = request.data
    logging.info(f'Alipay notify params: {params}')
    
    if not payment.verify_alipay_notification(params):
        logging.warning(f'Alipay notification verification failed. Alipay notify params: {params}')
        return Response('fail')
    order_id = params['out_trade_no']
    if order_id.startswith(SubscriptionOrder.ORDER_ID_PREFIX):
        subscription_order = SubscriptionOrder.objects.get(order_id=order_id)
        if subscription_order.paid_datetime:
            logging.warning(f'Order {order_id} was already paid')
            return Response('success')

        # if subscription_order.amount_str != params['total_amount']:
        #     logging.warning(f'Amount for order ID {order_id} does not match the Alipay order: {params["total_amount"]}')
        #     return Response('fail')
        subscription_order.paid_datetime = timezone.now()
        subscription_order.save()

        try:
            subscription = Subscription.objects.get(user_id=subscription_order.user.id)
        except Subscription.DoesNotExist:
            subscription = Subscription(user=subscription_order.user)
        
        current_expiry_datetime = subscription.expiry_datetime if subscription.expiry_datetime else subscription_order.paid_datetime
        subscription.expiry_datetime = current_expiry_datetime \
                                       + relativedelta(months=SUBSCRIPTION_PRODUCTS[subscription_order.product_id]['time_months'])
        subscription.save()
    elif order_id.startswith(ImageOrder.ORDER_ID_PREFIX):
        # 处理形象购买的订单
        image_order = ImageOrder.objects.get(order_id=order_id)
        if image_order.paid_datetime:
            logging.warning(f'Order {order_id} was already paid')
            return Response('success')
        image_order.paid_datetime = timezone.now()
        image_order.save()
        try:
            image = Image.objects.get(id=image_order.image_id)
            UserImage.objects.update_or_create(user=image_order.user, image=image)
        except Image.DoesNotExist:
            logging.warning(f'Image with ID {image_order.image_id} does not exist')
    elif order_id.startswith(EnvironmentOrder.ORDER_ID_PREFIX):
        # 处理背景购买的订单
        environment_order = EnvironmentOrder.objects.get(order_id=order_id)
        if environment_order.paid_datetime:
            logging.warning(f'Order {order_id} was already paid')
            return Response('success')
        environment_order.paid_datetime = timezone.now()
        environment_order.save()
        try:
            environment = Environment.objects.get(id=environment_order.environment_id)
            UserEnvironment.objects.update_or_create(user=environment_order.user, environment=environment)
        except Environment.DoesNotExist:
            logging.warning(f'Environment with ID {environment_order.environment_id} does not exist')
    else:
        logging.warning(f'Unrecognized order ID: {order_id}')
    return Response('success')
