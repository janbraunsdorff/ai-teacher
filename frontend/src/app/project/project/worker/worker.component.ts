import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Labler, ProjectService } from 'src/app/services/backend/project.service';

@Component({
  selector: 'app-worker',
  templateUrl: './worker.component.html',
  styleUrls: ['./worker.component.scss']
})
export class WorkerComponent implements OnInit {

  project_id: string = ''

  constructor(private currentRoute: ActivatedRoute, public service: ProjectService) { }


  ngOnInit(): void {
    this.currentRoute.parent?.params.subscribe((val) => {
      this.project_id = val['id']
      this.service.getWorker(this.project_id)
    })
  }

}
