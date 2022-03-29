import { Component, HostListener, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Class, ImageService } from 'src/app/services/backend/image.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-image-classification',
  templateUrl: './image-classification.component.html',
  styleUrls: ['./image-classification.component.scss']
})
export class ImageClassificationComponent implements OnInit {
  host = environment.host
  pid = ''
  img = ''
  selected = ''
  auto = false
  iid = ''

  key: string[] = '1234567890abcdefghijklmnopqrstuvwxyz'.split('')
  classes: Class[] = []

  constructor(public service: ImageService, private currentRoute: ActivatedRoute) { }

  ngOnInit(): void {
    this.service.classes.subscribe((res) => {
      if (res === null) {
        return
      }
      this.iid = res.id
      this.img = this.host + '/images/' + this.pid  +'/' +  res.id
      this.classes = res.classes

    })

    this.currentRoute.parent?.params.subscribe((val) => {
      this.pid = val['id']

      this.service.getNextClassification(val['id'])
    })
  }

  select(cid: string) {
    this.selected = cid

    if (this.auto) {
      this.label()
    }
  }

  label() {
    if (this.selected !== '') {
      console.log('send')
      this.service.classify(this.pid, this.iid, this.selected)
      this.service.getNextClassification(this.pid)     
    }
  }

  autoSubmit(event: any) {
    this.auto = event.checked
  }

  @HostListener('document:keypress', ['$event'])
  handleKeyboardEvent(event: KeyboardEvent) { 
    let key: string = event.key;

    if (key == 'Enter') {
      this.label()
    }else {
      const idx = this.key.findIndex(r => r == key)
      const cls =  this.classes[idx]
      if (cls != undefined) {
        this.selected = cls.name
      }  
      
      if (this.auto) {
        this.label()
      }
    }

  }



}
