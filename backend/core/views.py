from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import AccountRequestForm
from .models import Account

@login_required
def dashboard(request):
    active_accounts = Account.objects.filter(status='active')
    flagged_accounts = Account.objects.filter(risk_score__gte=70)
    pending_accounts = Account.objects.filter(status='pending')

    return render(request, 'core/dashboard.html', {
        'active_accounts': active_accounts,
        'flagged_accounts': flagged_accounts,
        'pending_accounts': pending_accounts,
    })

@login_required
def request_account(request):
    if request.method == 'POST':
        form = AccountRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AccountRequestForm()

    return render(request, 'core/request_account.html', {'form': form})
