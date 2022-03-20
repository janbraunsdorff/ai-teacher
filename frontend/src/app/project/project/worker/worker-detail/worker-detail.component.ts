import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Labler, ProjectService } from 'src/app/services/backend/project.service';

@Component({
  selector: 'app-worker-detail',
  templateUrl: './worker-detail.component.html',
  styleUrls: ['./worker-detail.component.scss']
})
export class WorkerDetailComponent implements OnInit {

  @Input() worker: Labler;
  project_id: string =  '';

  constructor(private currentRoute: ActivatedRoute, private service: ProjectService) { }

  ngOnInit(): void {

    this.currentRoute.parent?.params.subscribe((val) => {
      this.project_id = val['id']
    })
  }

  toggle() {
    this.service.toggleWorker(this.project_id, this.worker.id)
  }

}
