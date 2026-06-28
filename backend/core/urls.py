from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('compliance/', views.compliance_dashboard, name='compliance'),
    path('request-account/', views.request_account, name='request_account'),
    path('api/accounts/', views.api_accounts, name='api_accounts'),
    path('api/transactions/', views.api_transactions, name='api_transactions'),
]
