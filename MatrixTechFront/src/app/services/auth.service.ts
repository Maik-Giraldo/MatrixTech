import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LoginResponse } from '../shared/interfaces/login-response';
import { BehaviorSubject, Observable } from 'rxjs';
import { LoginRequest } from '../shared/interfaces/login-request';
import { environment } from 'src/environments/environment';
import { registerRequest } from '../shared/interfaces/register-request';
import { RegisterResponse } from '../shared/interfaces/register-response';
import { Router } from '@angular/router';
import { updateRequest } from '../shared/interfaces/update-request';
import { updateResponse } from '../shared/interfaces/update-reponse';
import { verifyTokenResponse } from '../shared/interfaces/verify-token-response';
import { DeleteResponse } from '../shared/interfaces/delete-response';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  readonly base_url: string;

  #dispatchIsLoggedIn: BehaviorSubject<boolean>;

  constructor(
    private _http: HttpClient,
    private _router: Router
  ) {
    this.base_url = environment.base_url;
    this.#dispatchIsLoggedIn = new BehaviorSubject<boolean>(this._isLoggedIn());
  }

  private _isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

  onLoggedIn(): Observable<boolean> {
    return this.#dispatchIsLoggedIn.asObservable();
  }

  loggedIn(){
    this.#dispatchIsLoggedIn.next(true);
  }

  register(request: registerRequest): Observable<RegisterResponse> {
    return this._http.post<RegisterResponse>(`${this.base_url}/users/register`, request);
  }

  login(request: LoginRequest): Observable<LoginResponse> {
    return this._http.post<LoginResponse>(`${this.base_url}/users/login`, request);
  }

  setToken(token: string) {
    localStorage.setItem('token', token);
  }

  logout() {
    localStorage.removeItem('token');
    this.#dispatchIsLoggedIn.next(false);
    this._router.navigate(['/login']);
  }

  updateUser(request: updateRequest): Observable<updateResponse> {
    return this._http.put<updateResponse>(`${this.base_url}/users`, request);
  }

  delete(): Observable<DeleteResponse> {
    return this._http.delete<DeleteResponse>(`${this.base_url}/users`);
  }

  verifyToken(): Observable<verifyTokenResponse> {
    return this._http.post<verifyTokenResponse>(`${this.base_url}/verify_token`, {});
  }
}
