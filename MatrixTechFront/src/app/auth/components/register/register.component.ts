import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { NotifierService } from 'angular-notifier';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit { 
  registerForm!: FormGroup;

  constructor(
    private _fb: FormBuilder,
    private _auth: AuthService,
    private _router: Router,
    private _notifier: NotifierService
  ) { }

  ngOnInit(): void {
    this.registerForm = this._fb.group({
      name: ['', [Validators.required]],
      last_name: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      phone_number: ['', [Validators.required, Validators.minLength(10), Validators.maxLength(10)]],
      city: ['', [Validators.required]],
      country: ['', [Validators.required]]

    })
  }
  
  registerUser() {
    if(this.registerForm.valid) {
      this._auth.register(this.registerForm.value).subscribe({
        next: (response: any) => {
          if(response.registered) {
            this._notifier.show({
              type: 'success',
              message: response.message
            })
            this._router.navigate(['/auth/login']);
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

  get name() {
    return this.registerForm.get('name');
  }

  get last_name() {
    return this.registerForm.get('last_name');
  }

  get email() {
    return this.registerForm.get('email');
  }

  get password() {
    return this.registerForm.get('password');
  }

  get phone_number() {
    return this.registerForm.get('phone_number');
  }

  get city() {
    return this.registerForm.get('city');
  }

  get country() {
    return this.registerForm.get('country');
  }

}
