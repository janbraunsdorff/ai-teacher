import { Component, Input, OnInit } from '@angular/core';
import { ImageMeta } from 'src/app/services/backend/project.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-image-details',
  templateUrl: './image-details.component.html',
  styleUrls: ['./image-details.component.scss']
})
export class ImageDetailsComponent implements OnInit {

  @Input() img: ImageMeta = {
    name: '',
    shape: '',
    tasks: [],
  };

  @Input() pid: string = ''
  open: boolean = false
  image_host = ''


  constructor() { }

  ngOnInit(): void {
  }

  toggle(){
    if (this.open) {
      this.image_host = ''
      this.open = false
    }else {
      this.image_host = environment.host + "/images/"+ this.pid +  "/" + this.img.name
      this.open = true 
    }
  }

}
