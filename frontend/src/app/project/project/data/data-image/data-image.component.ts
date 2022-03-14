import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ImageMeta, ProjectService } from 'src/app/services/backend/project.service';

@Component({
  selector: 'app-data-image',
  templateUrl: './data-image.component.html',
  styleUrls: ['./data-image.component.scss']
})
export class DataImageComponent implements OnInit {
  project_id: string = '';

  constructor(private currentRoute: ActivatedRoute, public service: ProjectService) { }

  ngOnInit(): void {
    this.currentRoute.parent?.params.subscribe((val) => {
      this.project_id = val['id']
    })

    this.service.getImageData(this.project_id);
  }

}
