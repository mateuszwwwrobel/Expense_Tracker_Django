from django.urls import path
from expenses import views

urlpatterns = [
    path('', views.ExpenseListView.as_view(), name='all_expenses'),
    path('<id>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('create', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('update/<id>', views.ExpenseUpdateView.as_view(), name='expense_update'),
    path('delete/<id>', views.ExpenseDeleteView.as_view(), name='expense_delete'),

]
