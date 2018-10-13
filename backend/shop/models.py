import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    tags = ArrayField(models.CharField(max_length=255))
    price = models.IntegerField()

    def __str__(self):
        return 'Product {}({})'.format(self.name or 'No name', self.id)


class Customer(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return 'Customer {}({})'.format(self.name or 'No name', self.pk)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return 'Order {}'.format(self.pk)
