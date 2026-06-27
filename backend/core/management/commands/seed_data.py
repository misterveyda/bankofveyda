from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Account, Transaction
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed sample accounts and transactions for Bank of Veyda'

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(username='sandbox-user', defaults={'email': 'sandbox@example.com'})

        account, created = Account.objects.get_or_create(
            account_number='VYDA0001',
            defaults={
                'owner': user,
                'balance': 12500,
                'status': 'active',
                'risk_score': 38,
                'compliance_clearance': True,
                'expires_at': timezone.now() + timezone.timedelta(days=30),
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created sample account VYDA0001.'))
        else:
            self.stdout.write(self.style.WARNING('Sample account already exists.'))

        Transaction.objects.get_or_create(
            account=account,
            amount=3250,
            transaction_type='deposit',
            description='Initial sandbox deposit',
        )

        Transaction.objects.get_or_create(
            account=account,
            amount=1200,
            transaction_type='transfer',
            description='Example outbound transfer',
        )

        self.stdout.write(self.style.SUCCESS('Seeded sample transactions.'))
