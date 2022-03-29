import { Component, Input, OnInit } from '@angular/core';
import { ImageService } from 'src/app/services/backend/image.service';
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
    results: {},
    org_name: ''
  };

  @Input() pid: string = ''
  open: boolean = false
  image_host = ''


  constructor(private service: ImageService) { }

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

  relabel(type: string){
    this.service.relabel(this.pid, this.img.name, type)
  }

}
