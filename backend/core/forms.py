from django import forms
from django.contrib.auth.models import User
from .models import Account

class AccountRequestForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Account
        fields = ['account_number', 'balance', 'expires_at', 'risk_score', 'device_fingerprint']
        widgets = {
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_account_number(self):
        account_number = self.cleaned_data['account_number']
        if Account.objects.filter(account_number=account_number).exists():
            raise forms.ValidationError('This account number is already in use.')
        return account_number

    def save(self, commit=True):
        user, created = User.objects.get_or_create(
            username=self.cleaned_data['username'],
            defaults={'email': self.cleaned_data['email']}
        )
        account = super().save(commit=False)
        account.owner = user
        account.status = 'pending'
        if commit:
            account.save()
        return account
