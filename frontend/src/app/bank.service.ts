import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

export interface CreateAccountRequest {
  account_holder_name: string;
  ttl_days?: number;
  creation_ip?: string | null;
  creation_device_fingerprint?: string | null;
}

export interface BurnerAccount {
  id: string;
  account_number: string;
  routing_number: string;
  account_holder_name: string;
  status: string;
  balance: number;
  available_balance: number;
  created_at: string;
  expires_at: string;
  ttl_days: number;
  days_until_expiry: number;
  risk_score: number;
  is_high_risk: boolean;
  is_flagged_for_review: boolean;
  stripe_account_id?: string | null;
  plaid_account_id?: string | null;
  creation_ip?: string | null;
  closed_at?: string | null;
  reason_for_closure?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class BankService {
  private apiUrl = environment.apiUrl;
  private authToken?: string;

  constructor(private http: HttpClient) {
    this.authToken = localStorage.getItem('auth_token') ?? undefined;
  }

  private getAuthHeaders(): HttpHeaders {
    let headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    if (this.authToken) {
      headers = headers.set('Authorization', `Bearer ${this.authToken}`);
    }
    return headers;
  }

  login(username: string, password: string): Observable<Token> {
    const body = new HttpParams()
      .set('username', username)
      .set('password', password)
      .set('grant_type', 'password');

    return this.http.post<Token>(`${this.apiUrl}/auth/token`, body.toString(), {
      headers: new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' }),
    });
  }

  setToken(token: string): void {
    this.authToken = token;
    localStorage.setItem('auth_token', token);
  }

  clearToken(): void {
    this.authToken = undefined;
    localStorage.removeItem('auth_token');
  }

  getToken(): string | undefined {
    return this.authToken;
  }

  createBurnerAccount(request: CreateAccountRequest): Observable<BurnerAccount> {
    return this.http.post<BurnerAccount>(`${this.apiUrl}/accounts/create`, request, {
      headers: this.getAuthHeaders(),
    });
  }

  getAccount(accountId: string): Observable<BurnerAccount> {
    return this.http.get<BurnerAccount>(`${this.apiUrl}/accounts/${accountId}`, {
      headers: this.getAuthHeaders(),
    });
  }
}
