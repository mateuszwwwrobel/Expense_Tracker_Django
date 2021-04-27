from django.db import models
from users.models import User

categories = (
    ('Food', 'Food'),
    ('Entertainment', 'Entertainment'),
    ('Bills', 'Bills'),
    ('Travel', 'Travel')
)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=15, choices=categories)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"{self.amount} - {self.category}"

    @classmethod
    def search_by_id(cls, id):
        return cls.objects.get(id=id)
