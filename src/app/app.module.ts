import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { MatCardModule, MatMenuModule, MatButtonModule, MatIconModule, MatGridListModule, MatDividerModule, MatChipsModule} from '@angular/material';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule }    from '@angular/forms';

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

const appRoutes: Routes = [
  // { path: 'crisis-center', component: CrisisListComponent },
  // { path: 'hero/:id',      component: HeroDetailComponent },
  {
    path: 'main',
    component: MainComponent,
    data: { title: 'Main' },
    children: [
      {path: 'home', component: HomeComponent},
      {path: 'campaignDetails/:id', component: CampaignDetailsComponent}
    ]
  },
  // {
  //   path: 'home',
  //   component: HomeComponent,
  //   data: { title: 'Home' }
  // },
  {
    path: 'profile',
    component: ProfileComponent,
    data: { title: 'Profile' }
  },
  // {
  //   path: 'campaignDetails/:id',
  //   component: CampaignDetailsComponent,
  //   data: { title: 'Campaign Details' }
  // },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  // { path: '',
  //   redirectTo: '/home',
  //   pathMatch: 'full'
  // },
  { path: '', component: MainComponent, canActivate: [AuthGuard] },
  // otherwise redirect to home
  { path: '**', redirectTo: '' }
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
    NotificationsComponent
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
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    )
  ],
  providers: [ 
    AuthGuard,
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
