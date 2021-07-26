
from django import forms
from django.db.models import Q

from expenses.models import Budget, Expense


class CreateBudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = ('name', 'currency')


class CreateHistoricalExpense(forms.ModelForm):

    class Meta:
        model = Expense
        fields = ('name', 'price', 'budget',  'category', 'created_at')
        labels = {
            'created_at': 'Date od Expense',
            'name': 'Expense name',
            'budget': 'Choose budget',
            'price': 'Expense price',
            'category': 'Select category',
        }

        user = None
        user_budgets = None

    def __init__(self, *args, **kwargs):
        self.user = args[-1].get('user')
        self.user_budgets = Budget.objects.filter(Q(users=self.user) | Q(created_by=self.user))
        super(CreateHistoricalExpense, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = self.user_budgets
        self.fields['created_at'].widget.attrs.update({'value': 'YYYY-MM-DD'})
