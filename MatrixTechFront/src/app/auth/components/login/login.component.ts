import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { NotifierService } from 'angular-notifier';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;

  constructor(
    private _fb: FormBuilder,
    private _authService: AuthService,
    private _router: Router,
    private _notifier: NotifierService
  ) { }

  ngOnInit(): void {
    this.loginForm = this._fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  login() {
    if(this.loginForm.valid){
      this._authService.login(this.loginForm.value).subscribe({
        next: (response) => {
          if(response.logged) {
            this._notifier.show({
              type: 'success',
              message: response.message
            })
            this._authService.setToken(response.token!);
            this._authService.loggedIn();
            this._router.navigate(['/home']);
          }else{
            this._notifier.show({
              type: 'error',
              message: response.message
            })
          }
        }
      })
    }
  }


  get email() {
    return this.loginForm.get('email');
  }
}
