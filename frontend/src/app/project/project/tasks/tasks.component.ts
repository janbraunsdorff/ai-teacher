import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProjectService, Task } from 'src/app/services/backend/project.service';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.scss']
})
export class TasksComponent implements OnInit {

  project_id: string = '';

  

  constructor(private currentRoute: ActivatedRoute, public service: ProjectService) { }


  ngOnInit(): void {
    this.currentRoute.parent?.params.subscribe((val) => {
      this.project_id = val['id']
      this.service.getProjectTasks(this.project_id)
    })

  }


  toggle(task_id: string) {
    this.service.toggle(this.project_id, task_id)
  }

}
