import { Component, OnInit } from '@angular/core';
import { OktaAuthService } from '@okta/okta-angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit {

  isAuthenticated: boolean;

  constructor(private oktaAuth: OktaAuthService, private router: Router) {
  }

  async ngOnInit() {
    this.isAuthenticated = await this.oktaAuth.isAuthenticated();
    this.oktaAuth.setFromUri('/main');
    // Subscribe to authentication state changes
    this.oktaAuth.$authenticationState.subscribe(
      (isAuthenticated: boolean)  => {
        this.isAuthenticated = isAuthenticated;
        if (!this.isAuthenticated) {
          this.oktaAuth.loginRedirect();
        }
    });
    if (!this.isAuthenticated) {
      this.oktaAuth.loginRedirect();
    }
  }
}
