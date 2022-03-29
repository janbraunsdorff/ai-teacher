import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { Segements } from 'src/app/models/datatypes';

@Component({
  selector: 'app-image-seg-ext',
  templateUrl: './image-seg-ext.component.html',
  styleUrls: ['./image-seg-ext.component.scss']
})
export class ImageSegExtComponent implements OnInit {

  img = 'assets/data/perso.jpeg'

  showEvent: Subject<string> = new Subject<string>();
  delete: Subject<void> = new Subject<void>();

  public segement: Segements[] = [
    {label: 'Firstname', segements: [], value: ''},
    {label: 'Lastname', segements: [], value: ''},
    {label: 'Birthday', segements: [], value: ''}
  ]

  public activate = ''
  public action = ''
  start: {x: number, y: number} = {x: -1, y: -1}


  constructor() { }

  ngOnInit(): void {
  }

  startDrawing(event: any) {
    this.start = event
  }

  endDrawing(event: any) {
    this.segement.filter(s => s.label === this.activate)[0].segements.push({start: this.start, end: event})
    this.start = {x: -1, y: -1}

    console.log(this.segement)
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
      console.log(this.activate)
      this.showEvent.next(this.activate)
    }
  }

  del(cls: string) {
    this.delete.next()
    this.segement.filter(s => s.label === cls)[0].segements = []
    this.action = ''
    this.activate = ''
  }

}
