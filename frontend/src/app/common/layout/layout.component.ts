import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/services/backend/user.service';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit {

  public user: string = ''

  constructor(private userService: UserService) {
  }
  
  
  ngOnInit(): void {
    this.userService.user.subscribe((user) => {
      this.user = user
    })

    this.userService.currentUser()
  }

  ngOnDestroy(): void {
  }


  logout() {
    this.userService.logout()
  }

}
