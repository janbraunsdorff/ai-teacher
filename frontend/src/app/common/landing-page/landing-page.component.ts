import { Component, OnInit } from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import { CreateProjectComponent } from 'src/app/project/create-project/create-project.component';
import { Project, ProjectService } from 'src/app/services/backend/project.service';


@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {


  constructor(public dialog: MatDialog, public service: ProjectService) { }

  ngOnInit(): void {
    this.service.getProjects()
  }

  openDialog() {
    const dialogRef = this.dialog.open(CreateProjectComponent, {
      width: '30em',
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(result);
      this.service.createProject(result)
    });
  }

}
