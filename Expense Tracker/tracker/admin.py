from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'type', 'category', 'payment_mode', 'date')
    list_filter = ('type', 'category', 'payment_mode', 'date')
    search_fields = ('description',)
    ordering = ('-date',)
