from django import forms
from django.contrib.auth.models import User

from expenses.models import Budget


class CreateBudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = ('name', 'currency')


