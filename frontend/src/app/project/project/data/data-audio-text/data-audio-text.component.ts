import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProjectService } from 'src/app/services/backend/project.service';

@Component({
  selector: 'app-data-audio-text',
  templateUrl: './data-audio-text.component.html',
  styleUrls: ['./data-audio-text.component.scss']
})
export class DataAudioTextComponent implements OnInit {

  project_id = ''

  constructor(public service: ProjectService, private currentRoute: ActivatedRoute) { }

  ngOnInit(): void {
    this.currentRoute.parent?.params.subscribe((val) => {
      this.project_id = val['id']
    })

    this.service.getAudioTextData(this.project_id);
  }

}
