import { Component } from '@angular/core';

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
}
