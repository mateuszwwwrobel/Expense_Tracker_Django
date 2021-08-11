from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Sum

categories = (
    ('Food', 'Food'),
    ('Takeaway', 'Takeaway'),
    ('Entertainment', 'Entertainment'),
    ('Bills', 'Bills'),
    ('Household Items', 'Household Items'),
    ('Other', 'Other'),
    ('Travel', 'Travel'),
)

currencies = (
    ('PLN', 'PLN'),
    ('GBP', 'GBP'),
    ('EUR', 'EUR'),
)


class Budget(models.Model):
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=3, choices=currencies)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by')
    users = models.ManyToManyField(User, related_name='users', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=15, choices=categories)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.price} - {self.category}"

    class Meta:
        ordering = ('created_at', )

    @classmethod
    def get_by_id(cls, id):
        try:
            expense = cls.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
        else:
            return expense

    @staticmethod
    def get_total_expenses_for_current_year(budget_id):
        today = datetime.today()
        expenses = Expense.objects.filter(budget=budget_id).filter(created_at__year=today.year)
        total = expenses.aggregate(total=Sum('price'))['total']
        if total is None:
            exp_sum = 0
        else:
            exp_sum = round(total, 2)
        return exp_sum

    @staticmethod
    def get_total_expenses_for_current_month(budget_id):
        today = datetime.today()
        expenses = Expense.objects.filter(budget=budget_id).filter(created_at__month=today.month)
        total = expenses.aggregate(total=Sum('price'))['total']
        if total is None:
            exp_sum = 0
        else:
            exp_sum = round(total, 2)
        return exp_sum
