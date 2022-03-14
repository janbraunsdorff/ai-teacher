import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, CanActivateChild, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { JwtHelperService } from "@auth0/angular-jwt";

@Injectable({
  providedIn: 'root'
})
export class AuthGuardService implements CanActivate, CanActivateChild{
  private helper;

  constructor(private router: Router) { 
    this.helper = new JwtHelperService();

  }
  canActivateChild(childRoute: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    return this.allowd();
  }

  allowd(): boolean {
    let auth = localStorage.getItem('auth') 

    if (auth === null || auth === '') {
      this.router.navigate(['/login'])
      return false
    }

    let data = JSON.parse(auth)
    if (Date.now() < data['expired_in']) {
      return true
    }

    this.router.navigate(['/login'])
    return false;
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    return this.allowd();
    
  }

}
