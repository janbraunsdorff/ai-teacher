import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ProjectService } from 'src/app/services/backend/project.service';

@Component({
  selector: 'app-classes',
  templateUrl: './classes.component.html',
  styleUrls: ['./classes.component.scss']
})
export class ClassesComponent implements OnInit {

  constructor(public service: ProjectService, private currentRoute: ActivatedRoute) { }

  ngOnInit(): void {
    this.currentRoute.parent?.params.subscribe((val) => {
      const project_id = val['id']
      this.service.getTargets(project_id)
    })
  }

}
