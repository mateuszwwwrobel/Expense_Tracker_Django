from django.urls import path
from expenses.views import (
    ExpenseListView,
    ExpenseDetailView,
    ExpenseCreateView,
    ExpenseUpdateView,
    ExpenseDeleteView,
    TestView)

urlpatterns = [
    path('', ExpenseListView.as_view(), name='all_expenses'),
    path('<id>/', ExpenseDetailView.as_view(), name='expense_detail'),
    path('create', ExpenseCreateView.as_view(), name='expense_create'),
    path('update/<id>', ExpenseUpdateView.as_view(), name='expense_update'),
    path('delete/<id>', ExpenseDeleteView.as_view(), name='expense_delete'),
    path('test', TestView.as_view(), name='test_view'),


]
