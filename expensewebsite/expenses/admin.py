from django.contrib import admin
from .models import Expense, Category


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'description', 'owner', 'category')
    search_fields = ('date', 'description', 'category')


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
