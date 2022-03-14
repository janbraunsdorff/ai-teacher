import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProjectService } from 'src/app/services/backend/project.service';


@Component({
  selector: 'app-data',
  templateUrl: './data.component.html',
  styleUrls: ['./data.component.scss']
})
export class DataComponent implements OnInit {
  project_id: string = '';
  file: File | null = null
  kind: string = ''
  progess: number | null = null

  kinds = [
    {view: 'Image', value: 'image'},
    {view: 'Text', value: 'text'},
    {view: 'Voice', value: 'voice'},
  ]

  constructor(private currentRoute: ActivatedRoute, private service: ProjectService) { }

  ngOnInit(): void {
    this.currentRoute.parent?.params.subscribe((val) => {
      this.project_id = val['id']
    })
  }

  selectFile(files: FileList | null) {
    this.file = files![0]
  }

  upload(){
    if (this.file != null){
      this.service.progess.subscribe((progress) => {
        this.progess = progress
      })
      this.service.uploadData(this.file, this.project_id, this.kind)
    }
  }

}
