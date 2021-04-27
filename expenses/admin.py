from django.contrib import admin
from expenses.models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'currency', 'category', 'updated_at')
    search_fields = ('category', )
    list_per_page = 25
    list_display_links = ('id', 'amount')
