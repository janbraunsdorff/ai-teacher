import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ProjectService } from 'src/app/services/backend/project.service';

@Component({
  selector: 'app-classes',
  templateUrl: './classes.component.html',
  styleUrls: ['./classes.component.scss']
})
export class ClassesComponent implements OnInit {

  name: string = ''
  desc: string = ''

  project_id: string = ''

  constructor(public service: ProjectService, private currentRoute: ActivatedRoute) { }

  ngOnInit(): void {
    this.currentRoute.parent?.params.subscribe((val) => {
      this.project_id = val['id']
      this.service.get_classes(this.project_id)
    })
  }

  save(){
    this.service.add_class(this.project_id, this.name, this.desc)
    this.name = ''
    this.desc = ''
  }

  deleteClass(cid: string){
    this.service.deleteClass(this.project_id, cid)
  }

}
