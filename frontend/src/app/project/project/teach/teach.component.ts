import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProjectService } from 'src/app/services/backend/project.service';

@Component({
  selector: 'app-teach',
  templateUrl: './teach.component.html',
  styleUrls: ['./teach.component.scss']
})
export class TeachComponent implements OnInit {
  pid: string = ''

  nameToPath = new Map<string, string>([
    ["Image Classification", "img-classification"],
    ["Image Bounding Box", "img-bounding-box"],
    ["Image Entity Extraction", "img-extraction"],
    ["Audio Recording", "recording"],
    ["Text Entity Extraction", "text-extraction"],
  ])

  constructor(private currentRoute: ActivatedRoute, public service: ProjectService) { }

  ngOnInit(): void {
    this.currentRoute.parent?.params.subscribe((val) => {
      this.pid = val['id']
      this.service.getExcercies(val['id'])
    })
  }

}
