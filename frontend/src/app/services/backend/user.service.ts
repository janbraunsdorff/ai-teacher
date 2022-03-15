import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { environment } from '../../../environments/environment'


@Injectable({
  providedIn: 'root'
})
export class UserService {

  public user = new Subject<string>()
  public err = new Subject<string>()


  constructor(private client: HttpClient, private router: Router) { }

  login(user: string, pass: string) {
    let formData = new FormData();
    formData.append("username", user)
    formData.append("password", pass)
    this.client.post<Token>
      (environment.host + "/user/login", formData)
      .subscribe( (res) =>{
        localStorage.setItem("auth", JSON.stringify(res))
        this.currentUser()
        this.err.next('')
        this.router.navigate(['/'])
      }, (err) => {
        this.router.navigate(['/login'])
        if (err.status == 401){
          this.err.next(err.error.detail)
        }
      })
  }

  register(alias: string, name: string, password_clear: string) {
    this.client.post<{access_token: string,  token_type: string}>
      (environment.host + "/user/register", {alias, name, password: password_clear})
      .subscribe( (res) =>{
        localStorage.setItem("auth", JSON.stringify(res))
        this.currentUser()
        this.err.next('')
        this.router.navigate(['/'])
      }, (err) => {
        this.router.navigate(['/login'])
        if (err.status == 422){
          this.err.next(err.error.detail)
        }
      })
  }

  logout() {
    localStorage.removeItem("auth")
    this.router.navigate(['/'])
  }


  currentUser() {
    let auth = localStorage.getItem("auth")
    let user = ''
    if (!(auth == null || auth == '')) {
      user = JSON.parse(auth)["alias"]
    }
    this.user.next(user)
  }

}

interface Token {
  expired_in: number
  alias: string,
  roles: string[]
}
