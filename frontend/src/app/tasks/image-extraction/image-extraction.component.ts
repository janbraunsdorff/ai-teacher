import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ImageService } from 'src/app/services/backend/image.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-image-extraction',
  templateUrl: './image-extraction.component.html',
  styleUrls: ['./image-extraction.component.scss']
})
export class ImageExtractionComponent implements OnInit {

  img = ''
  pid = ''
  host = environment.host



  entities: {label: string, value: string, class_id: string, img_id: string}[] = []

  constructor(private service: ImageService, private currentRoute: ActivatedRoute) { }

  ngOnInit(): void {
    this.service.extraction.subscribe(res => {
      this.entities = []
      res.classes.forEach(c => this.entities.push({label: c.name, value: '', class_id: c.id, img_id: res.id}))
      this.img = this.host + '/images/' + this.pid  +'/' +  res.id

    })

    this.currentRoute.parent?.params.subscribe((val) => {
      this.pid = val['id']

      this.service.getNextExtraction(val['id'])
    })
  }

  send() {
    this.entities.forEach(e => this.service.extract(this.pid, e.img_id, e.class_id, e.value))
    this.service.getNextExtraction(this.pid)

  }

}
