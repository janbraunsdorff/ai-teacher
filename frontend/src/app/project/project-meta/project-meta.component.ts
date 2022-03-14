import { Component, Input, OnInit } from '@angular/core';
import { Project } from 'src/app/services/backend/project.service';

@Component({
  selector: 'app-project-meta',
  templateUrl: './project-meta.component.html',
  styleUrls: ['./project-meta.component.scss']
})
export class ProjectMetaComponent implements OnInit {

  @Input() project: Project = {
    name: '',
    id: '',
    created: ''
  }

  constructor() { }

  ngOnInit(): void {
  }

}
