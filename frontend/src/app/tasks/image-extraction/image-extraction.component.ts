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
  width = 100



  entities: {label: string, value: string, img_id: string}[] = []

  constructor(private service: ImageService, private currentRoute: ActivatedRoute) { }

  ngOnInit(): void {
    this.service.extraction.subscribe(res => {
      this.entities = []
      this.width = res.width
      res.classes.forEach(c => this.entities.push({label: c.name, value: '', img_id: res.id}))
      this.img = this.host + '/images/' + this.pid  +'/' +  res.id

    })

    this.currentRoute.parent?.params.subscribe((val) => {
      this.pid = val['id']

      this.service.getNextExtraction(val['id'])
    })
  }

  send() {
    const payload: {id: string, res: {lable: string, value: string}[]} = {id: this.entities[0].img_id, res: []}
    this.entities.forEach(e => payload.res.push({lable: e.label, value: e.value}))
    this.service.extract(this.pid, payload)
  }

}
