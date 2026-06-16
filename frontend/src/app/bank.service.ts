import { HttpClient } from '@angular/common/http';
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

  constructor(private http: HttpClient) {}

  createBurnerAccount(request: CreateAccountRequest): Observable<BurnerAccount> {
    return this.http.post<BurnerAccount>(`${this.apiUrl}/accounts/create`, request);
  }

  getAccount(accountId: string): Observable<BurnerAccount> {
    return this.http.get<BurnerAccount>(`${this.apiUrl}/accounts/${accountId}`);
  }
}
