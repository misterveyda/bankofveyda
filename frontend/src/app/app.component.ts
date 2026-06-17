import { Component } from '@angular/core';
import { BankService, BurnerAccount, CreateAccountRequest } from './bank.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Bank of Veyda';
  tagline = 'A sandbox bank built for compliance experimentation.';
  metrics = [
    { label: 'Temporary accounts', value: 128 },
    { label: 'Risk flags', value: 22 },
    { label: 'Audit alerts', value: 14 },
    { label: 'KYC failures', value: 5 }
  ];

  username = 'demo';
  password = 'demo123';
  accountHolderName = '';
  ttlDays = 30;
  createdAccount: BurnerAccount | null = null;
  errorMessage = '';
  authMessage = '';
  isAuthenticated = false;

  constructor(private bankService: BankService) {
    this.isAuthenticated = !!this.bankService.getToken();
  }

  login(): void {
    this.errorMessage = '';
    this.authMessage = '';
    this.bankService.login(this.username, this.password).subscribe({
      next: (token) => {
        this.bankService.setToken(token.access_token);
        this.isAuthenticated = true;
        this.authMessage = 'Authenticated successfully. You may now create an account.';
      },
      error: (error) => {
        console.error('Login failed', error);
        this.errorMessage = error?.error?.detail || 'Unable to login. Please verify credentials.';
      }
    });
  }

  createAccount(): void {
    this.errorMessage = '';
    this.createdAccount = null;

    const payload: CreateAccountRequest = {
      account_holder_name: this.accountHolderName,
      ttl_days: this.ttlDays,
    };

    this.bankService.createBurnerAccount(payload).subscribe({
      next: (account) => {
        this.createdAccount = account;
        this.accountHolderName = '';
      },
      error: (error) => {
        console.error('Account creation failed', error);
        this.errorMessage =
          error?.error?.detail ||
          error?.message ||
          'Unable to create account. Confirm that the backend is running and accessible.';
      }
    });
  }
}
