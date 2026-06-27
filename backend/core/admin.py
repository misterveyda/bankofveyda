from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'owner', 'status', 'balance', 'risk_score', 'compliance_clearance', 'expires_at')
    list_filter = ('status', 'compliance_clearance')
    search_fields = ('account_number', 'owner__username')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'created_at', 'flagged')
    list_filter = ('transaction_type', 'flagged')
    search_fields = ('account__account_number', 'description')
