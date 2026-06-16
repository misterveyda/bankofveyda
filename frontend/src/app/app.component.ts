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

  accountHolderName = '';
  ttlDays = 30;
  createdAccount: BurnerAccount | null = null;
  errorMessage = '';

  constructor(private bankService: BankService) {}

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
