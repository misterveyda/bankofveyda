import { Component } from '@angular/core';
import { BankService, Token } from './bank.service';

@Component({
  selector: 'app-login',
  template: `
    <section class="login-card">
      <h2>Sign in</h2>
      <form (ngSubmit)="login()" class="login-form">
        <label>
          Username
          <input type="text" [(ngModel)]="username" name="username" required />
        </label>

        <label>
          Password
          <input type="password" [(ngModel)]="password" name="password" required />
        </label>

        <button type="submit">Login</button>
      </form>

      <div class="error-message" *ngIf="errorMessage">{{ errorMessage }}</div>
      <div class="success-message" *ngIf="isAuthenticated">Logged in as {{ username }}</div>
    </section>
  `,
  styles: [
    `.login-card { margin-bottom: 2rem; padding: 1.5rem; border-radius: 16px; background: #0f172a; color: #ffffff; }`,
    `.login-form label { display: block; margin-bottom: 1rem; }`,
    `.login-form input { width: 100%; padding: 0.75rem; margin-top: 0.5rem; border-radius: 8px; border: 1px solid #334155; }`,
    `.login-form button { padding: 0.85rem 1.2rem; border: none; border-radius: 999px; background: #38bdf8; color: #0f172a; cursor: pointer; }`,
    `.error-message { margin-top: 1rem; color: #f87171; }`,
    `.success-message { margin-top: 1rem; color: #86efac; }
`  ]
})
export class LoginComponent {
  username = 'demo';
  password = 'demo123';
  errorMessage = '';
  isAuthenticated = false;

  constructor(private bankService: BankService) {}

  login(): void {
    this.errorMessage = '';
    this.bankService.login(this.username, this.password).subscribe({
      next: (token: Token) => {
        this.bankService.setToken(token.access_token);
        this.isAuthenticated = true;
      },
      error: (error) => {
        console.error('Login failed', error);
        this.errorMessage = error?.error?.detail || 'Unable to login. Please verify credentials.';
      }
    });
  }
}
