from django.test import TestCase
from django.contrib.auth.models import User
from .models import Account


class AccountModelTest(TestCase):
    def test_account_creation(self):
        user = User.objects.create_user(username='tester', password='password')
        account = Account.objects.create(
            owner=user,
            account_number='TEST123456',
            balance=1000,
            status='active',
            compliance_clearance=True,
        )

        self.assertEqual(str(account), 'TEST123456 (tester)')
        self.assertEqual(account.balance, 1000)
