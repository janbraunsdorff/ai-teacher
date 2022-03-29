import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subject, Subscription } from 'rxjs';
import { Segements } from 'src/app/models/datatypes';
import { ImageService } from 'src/app/services/backend/image.service';
import { ProjectService } from 'src/app/services/backend/project.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-image-segementation',
  templateUrl: './image-segementation.component.html',
  styleUrls: ['./image-segementation.component.scss']
})
export class ImageSegementationComponent implements OnInit, OnDestroy  {
  sub_class: Subscription| null = null
  host = environment.host


  img = ''
  pid = ''
  img_id = ''

  showEvent: Subject<string> = new Subject<string>();
  delete: Subject<void> = new Subject<void>();

  public segement: Segements[] = []

  public activate = ''
  public action = ''
  start: {x: number, y: number} = {x: -1, y: -1}


  constructor(private service: ProjectService, private image_service: ImageService,  private currentRoute: ActivatedRoute) { }

  ngOnDestroy(): void {
    this.sub_class?.unsubscribe()
  }

  ngOnInit(): void {
    this.image_service.bouding.subscribe( res => {
      this.img_id = res.id
      this.img = this.host + '/images/' + this.pid  +'/' + res.id;
      this.segement = []

      this.activate = ''
      this.action = ''
      this.start = {x: -1, y: -1}

      for (let clazz of res.classes) {        
        this.segement.push({label: clazz.name, segements: []})
      }
    })

    this.currentRoute.parent?.params.subscribe((val) => {
      this.pid = val['id']
      this.image_service.getNextBoudingBox(this.pid)
    })

    
  }

  startDrawing(event: any) {
    this.start = event
  }

  endDrawing(event: any) {
    this.segement.filter(s => s.label === this.activate)[0].segements.push({start: this.start, end: event})
    this.start = {x: -1, y: -1}
  }

  draw(cls: string) {
    if (this.action === 'draw' && this.activate === cls) {
      this.action = ''
      this.activate = ''
      this.start = {x: -1, y: -1}
      this.delete.next()
    }else {
      this.delete.next()
      this.action = 'draw'
      this.activate = cls

    }
  }

  show(cls: string) {
    this.delete.next()
    this.start = {x: -1, y: -1}
    if (this.action === 'show' && this.activate === cls) {
      this.action = ''
      this.activate = ''
    }else {
      this.action = 'show'
      this.activate = cls
      this.showEvent.next(this.activate)
    }
  }

  del(cls: string) {
    this.delete.next()
    this.segement.filter(s => s.label === cls)[0].segements = []
    this.action = ''
    this.activate = ''
  }

  send(){
    this.segement.forEach(s => this.image_service.boundingbox(this.pid, this.img_id, s.segements[0], s.value))
    this.image_service.getNextBoudingBox(this.pid)

  }
 
}