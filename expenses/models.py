from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


categories = (
    ('Food', 'Food'),
    ('Entertainment', 'Entertainment'),
    ('Bills', 'Bills'),
    ('Travel', 'Travel')
)

currencies = (
    ('PLN', 'PLN'),
    ('GBP', 'GBP'),
)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=15, choices=categories)
    currency = models.CharField(max_length=3, choices=currencies)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount} {self.currency} - {self.category}"

    @classmethod
    def get_by_id(cls, id):
        try:
            expense = cls.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
        else:
            return expense
