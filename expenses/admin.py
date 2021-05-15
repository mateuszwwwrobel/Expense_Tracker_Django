from django.contrib import admin
from expenses.models import Expense, Budget


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'category', 'updated_at')
    list_per_page = 25
    list_display_links = ('id', 'price')


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'currency')
    list_per_page = 25
    list_display_links = ('id', 'name')
