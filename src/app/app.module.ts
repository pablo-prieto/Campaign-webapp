import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { MatCardModule, MatMenuModule, MatButtonModule, MatIconModule, MatGridListModule, MatDividerModule, MatChipsModule, MatToolbarModule } from '@angular/material';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule }    from '@angular/forms';

import { OktaCallbackComponent, OktaAuthModule } from '@okta/okta-angular';
import { AuthInterceptor } from './shared/okta/auth.interceptor';

import { AppComponent } from './app.component';
import { ProfileComponent } from './profile/profile.component';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ProfileTabComponent } from './profile-tab/profile-tab.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { AlertComponent } from './alert/alert.component';

import { AlertService, AuthenticationService, UserService, CampaignService } from './services/index';
import { AuthGuard } from './guard/index';
import { JwtInterceptor } from './helpers';

// used to create fake backend
import { fakeBackendProvider } from './helpers';
import { CampaignDetailsComponent } from './campaign-details/campaign-details.component';
import { MainComponent } from './main/main.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { LoginPageComponent } from './login-page/login-page.component';

const config = {
  issuer: 'https://dev-801865.oktapreview.com/oauth2/default',
  redirectUri: 'http://localhost:4200/implicit/callback',
  clientId: '0oaj4w3zwcvrYSBuH0h7'
};

const appRoutes: Routes = [
  {
    path: 'main',
    component: MainComponent,
    data: { title: 'Main' },
    children: [
      {path: 'home', component: HomeComponent},
      {path: 'campaignDetails/:id', component: CampaignDetailsComponent}
    ]
  },
  {
    path: 'implicit/callback',
    component: OktaCallbackComponent
  },
  {
    path: 'profile',
    component: ProfileComponent,
    data: { title: 'Profile' }
  },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  // { path: '', component: MainComponent, canActivate: [AuthGuard] },
  {path: '', redirectTo: '/main', pathMatch: 'full'},
  {
    path: 'login-page',
    component: LoginPageComponent
  },
  // otherwise redirect to home
  { path: '**', redirectTo: '/main' }
];

@NgModule({
  declarations: [
    AppComponent,
    ProfileComponent,
    HomeComponent,
    ProfileTabComponent,
    LoginComponent,
    RegisterComponent,
    AlertComponent,
    CampaignDetailsComponent,
    MainComponent,
    NotificationsComponent,
    LoginPageComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatCardModule,
    MatMenuModule,
    MatButtonModule,
    MatIconModule,
    MatGridListModule,
    MatDividerModule,
    MatChipsModule,
    MatToolbarModule,
    OktaAuthModule.initAuth(config),
    RouterModule.forRoot(
      appRoutes
      // { enableTracing: true } // <-- debugging purposes only
    )
  ],
  providers: [ 
    // AuthGuard,
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    AlertService,
    AuthenticationService,
    UserService,
    CampaignService,
    {
        provide: HTTP_INTERCEPTORS,
        useClass: JwtInterceptor,
        multi: true
    },

    // provider used to create fake backend
    fakeBackendProvider
   ],
  bootstrap: [AppComponent]
})
export class AppModule { }
