from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F
import time
import datetime
from django.db import transaction
from django.core.cache import cache
from django.conf import settings

@shared_task(base=Singleton)
def set_price(subscription_id):
    from .models import Subscriptions

    with transaction.atomic():
        subscription = Subscriptions.objects.select_for_update().filter(id=subscription_id).annotate(
        anotated_price=F('service__full_price') -
            F('service__full_price') * F('plan__discount') / 100.00).first()

        subscription.price = subscription.anotated_price
        subscription.save()
    cache.delete(settings.PRICE_CACHE_NAME)

@shared_task(base=Singleton)
def set_comment(subscription_id):
    from .models import Subscriptions

    with transaction.atomic():
        subscription = Subscriptions.objects.select_for_update().get(id=subscription_id)
        subscription.comment = str(datetime.datetime.now())
        subscription.save()
    cache.delete(settings.PRICE_CACHE_NAME)
