from django.db import models
from django.core.validators import MaxValueValidator
from app.models import Client
from .recivers import delete_chache_total_sum
from .tasks import set_price, set_comment
from django.db.models.signals import post_delete

class Service(models.Model):
    name = models.CharField(max_length=100)
    full_price = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price
        
    def save(self, *args, **kwargs):
        if self.full_price != self.__full_price:
            for subscriprion in self.subscriptions.all():
                set_price.delay(subscriprion.id)
                set_comment.delay(subscriprion.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'name: {self.name}'


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount'),
    )
    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount = models.PositiveIntegerField(default=0,
                                           validators=[MaxValueValidator(100)]
                                          )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discoutn = self.discount
        
    def save(self, *args, **kwargs):
        if self.discount != self.__discoutn:
            for subscriprion in self.subscriptions.all():
                set_price.delay(subscriprion.id)
                set_comment.delay(subscriprion.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'plan: {self.plan_type} discount: {self.discount}' 


class Subscriptions(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=255, default='', db_index=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__price = self.price


    def save(self, *args, **kwargs):
        if self.__price != self.price:
            set_price.delay(self.id)
            set_comment.delay(self.id)
        creating = not bool(self.id)
        result = super().save(*args, **kwargs)
        # if creating:
        #     set_price.delay(self.id)
        return result

    def __str__(self):
        return f'client: {self.client} service{self.service} paln{self.plan} price:{self.price}'


post_delete.connect(delete_chache_total_sum, sender=Subscriptions)