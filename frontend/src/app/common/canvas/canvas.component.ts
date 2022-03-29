import { AfterViewInit, Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { Observable } from 'rxjs';
import { Segements } from 'src/app/models/datatypes';

@Component({
  selector: 'app-canvas',
  templateUrl: './canvas.component.html',
  styleUrls: ['./canvas.component.scss']
})
export class CanvasComponent implements AfterViewInit, OnInit {
  @Output('startDrawing') startDrawing: EventEmitter<any> = new EventEmitter();
  @Output('endDrawing') endDrawing: EventEmitter<any> = new EventEmitter();

  @ViewChild('img') img: ElementRef;
  @ViewChild('can') can: ElementRef;

  @Input('action') action: string;
  @Input('image') image: string;
  @Input('activate') activate: string;
  @Input('start') start: {x: number, y:number};
  @Input('segement') segement: Segements[];
  @Input('showEvent') showEvent: Observable<string>;
  @Input('delete') delete: Observable<void>;
  @Input('width') width: number;
  @Input('height') height: number;
  
  ctx: any = {}


  constructor() { }

  ngAfterViewInit(): void {
    this.showEvent?.subscribe((cls: string) => this.show(cls))
    this.delete?.subscribe(() => this.del())
  }

  ngOnInit(): void {
  }

  public initCanvas() {
    this.ctx = this.can?.nativeElement.getContext("2d")
    this.ctx.canvas.width = this.img?.nativeElement.offsetWidth
    this.ctx.canvas.height = this.img?.nativeElement.offsetHeight
    this.ctx.strokeStyle = 'red'
  }

  public mark(e: any) {
    if (this.action !== 'draw') {
      return
    }
    var rect = e.target.getBoundingClientRect();
    var x = e.clientX - rect.left;
    var y = e.clientY - rect.top;

    if (this.start.y !== -1 &&  this.start.x !== -1) {
      let end =  {'x': x, 'y':y}
      this.endDrawing.emit(end)
    }else {
      let start = {'x': x, 'y':y}
      this.startDrawing.emit(start)
    }
  }

  show(cls: string) {
    this.del()
    this.segement.filter(s => s.label === cls)[0].segements.forEach(s => {
      this.ctx.beginPath();

      this.ctx.moveTo(s.start.x, s.start.y);
      this.ctx.lineTo(s.start.x, s.end.y);
      this.ctx.lineTo(s.end.x, s.end.y);
      this.ctx.lineTo(s.end.x, s.start.y);
      this.ctx.lineTo(s.start.x, s.start.y);
      this.ctx.stroke();
    })
    
  }

  del() {
    this.ctx.clearRect(0, 0, 10000, 10000)
  }


  preview(e: any) {
    if (this.action !== 'draw') {
      return
    }

    if (!(this.start.y !== -1 &&  this.start.x !== -1)) {
      return
    }

    this.ctx.clearRect(0, 0, 10000, 10000)
    var rect = e.target.getBoundingClientRect();
    var y = e.clientY - rect.top;
    var x = e.clientX - rect.left; 
    this.ctx.beginPath();

    this.ctx.moveTo(this.start.x, this.start.y);
    this.ctx.lineTo(this.start.x, y);
    this.ctx.lineTo(x, y);
    this.ctx.lineTo(x, this.start.y);
    this.ctx.lineTo(this.start.x, this.start.y);
    this.ctx.stroke();
  }

}
