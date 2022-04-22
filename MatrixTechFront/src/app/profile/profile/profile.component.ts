import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { NotifierService } from 'angular-notifier';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit, AfterViewInit {
  @ViewChild('inputImage') inputImage!: ElementRef<HTMLElement>;
  updateForm!: FormGroup;

  constructor(
    private _fb: FormBuilder,
    private _auth: AuthService,
    private _router: Router,
    private _notifier: NotifierService
  ) { 
  }

  ngOnInit(): void {
    this.updateForm = this._fb.group({
      name: ['', [Validators.required]],
      last_name: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password: [],
      img_profile: [],
      phone_number: ['', [Validators.required, Validators.minLength(10), Validators.maxLength(10)]],
      city: ['', [Validators.required]],
      country: ['', [Validators.required]]
    })

    const token = localStorage.getItem('token');

    if(token) {
      this._auth.verifyToken().subscribe({
        next: (response) => {
          if(response.verified) {
            this._auth.loggedIn();
            this.updateForm.patchValue(response.data!);
          }else{
            this._router.navigate(['/login']);
          }
        }
      })
    }
  }

  ngAfterViewInit(): void {
    this.inputImage.nativeElement.onchange = (event: any) => {
      if(event.target.files && event.target.files[0]) {
        const reader = new FileReader();
        reader.onload = (e: any) => {
          this.img_profile?.setValue(e.target.result);
        }
        reader.readAsDataURL(event.target.files[0]);
      }
    }
  }

  updateUser() {
    if(this.updateForm.valid){
      if(this.updateForm.value.img_profile.includes('http')){
        this.updateForm.value.img_profile = null;
      }
      this._auth.updateUser(this.updateForm.value).subscribe({
        next: (response) => {
          if(response.updated) {
            this._notifier.show({
              type: 'success',
              message: response.message
            })
            this.updateForm.patchValue(response.data!);
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
    return this.updateForm.get('name');
  }

  get last_name() {
    return this.updateForm.get('last_name');
  }

  get email() {
    return this.updateForm.get('email');
  }

  get password() {
    return this.updateForm.get('password');
  }

  get phone_number() {
    return this.updateForm.get('phone_number');
  }

  get city() {
    return this.updateForm.get('city');
  }

  get country() {
    return this.updateForm.get('country');
  }

  get img_profile() {
    return this.updateForm.get('img_profile');
  }
}
