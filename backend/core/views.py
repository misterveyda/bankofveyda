from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from .forms import AccountRequestForm
from .auth_forms import LoginForm, SignupForm
from .models import Account, Transaction


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    active_accounts = Account.objects.filter(status='active')
    flagged_accounts = Account.objects.filter(risk_score__gte=70)

    return render(request, 'core/dashboard.html', {
        'active_accounts': active_accounts,
        'flagged_accounts': flagged_accounts,
    })


@login_required(login_url='login')
def compliance_dashboard(request):
    total_accounts = Account.objects.count()
    active_count = Account.objects.filter(status='active').count()
    frozen_count = Account.objects.filter(status='frozen').count()
    flagged_count = Account.objects.filter(risk_score__gte=70).count()

    high_risk = Account.objects.filter(risk_score__gte=80).order_by('-risk_score')[:10]
    recent_transactions = Transaction.objects.filter(flagged=True).order_by('-created_at')[:10]

    total_volume = Transaction.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    metrics = {
        'total_accounts': total_accounts,
        'active_count': active_count,
        'frozen_count': frozen_count,
        'flagged_count': flagged_count,
        'total_volume': total_volume,
    }

    return render(request, 'core/compliance.html', {
        'metrics': metrics,
        'high_risk': high_risk,
        'recent_transactions': recent_transactions,
    })


@login_required(login_url='login')
def request_account(request):
    if request.method == 'POST':
        form = AccountRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AccountRequestForm()

    return render(request, 'core/request_account.html', {'form': form})


@login_required(login_url='login')
def api_accounts(request):
    accounts = Account.objects.all().values(
        'id',
        'account_number',
        'balance',
        'status',
        'risk_score',
        'compliance_clearance',
        'created_at',
        'expires_at',
    )
    return JsonResponse({'accounts': list(accounts)})


@login_required(login_url='login')
def api_transactions(request):
    transactions = Transaction.objects.all().values(
        'id',
        'account__account_number',
        'amount',
        'transaction_type',
        'created_at',
        'flagged',
        'description',
    )
    return JsonResponse({'transactions': list(transactions)})
