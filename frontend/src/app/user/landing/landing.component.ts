import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/services/backend/user.service';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.scss']
})
export class LandingComponent implements OnInit {
  registerName: string = '';
  registerAlias: string = '';
  registerPasswordClear: string = '';

  loginAlias: string = '';
  loginPasswordClear: string = '';

  msg = ""


  constructor(private serive: UserService) { }

  ngOnInit(): void {
    this.serive.err.subscribe((err) => {
      this.msg = err
    })
  }

  login() {
    this.serive.login(this.loginAlias, this.loginPasswordClear)
  }

  register() {
    this.serive.register(this.registerAlias, this.registerName, this.registerPasswordClear)
  }

}
