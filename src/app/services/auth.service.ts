import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class AuthService {
    constructor(private http: HttpClient) { }

    isUserLoggedIn: boolean;

    getStatus(): boolean {
        console.log('auth status = ', this.isUserLoggedIn);
        if (this.isUserLoggedIn) {
            return true;
        }
        else return false;
    }

    setStatus( isLoggedIn) {
        console.log('auth status = ', isLoggedIn);
        this.isUserLoggedIn = isLoggedIn;
    }
}