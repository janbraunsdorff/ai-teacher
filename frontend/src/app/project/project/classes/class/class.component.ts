import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProjectService } from 'src/app/services/backend/project.service';

@Component({
  selector: 'app-class',
  templateUrl: './class.component.html',
  styleUrls: ['./class.component.scss']
})
export class ClassComponent implements OnInit {
  @Input() class: any;
  name: string = ''
  desc: string = ''

  project_id: string = ''

  constructor(private currentRoute: ActivatedRoute, private projectService: ProjectService) { }

  ngOnInit(): void {
    this.currentRoute.parent?.params.subscribe((val) => {
      this.project_id = val['id']
    })
  }

  save(id: string){
    const paylooad = {"task": id, "name": this.name, "describtion": this.desc}
    console.log(paylooad)
    this.projectService.postTask(this.project_id, paylooad)
    
  }

  deleteClass(id: string, name: string, desc: string){
    const paylooad = {"task": id, "name": name, "describtion": desc}
    this.projectService.deleteTask(this.project_id, paylooad)
  }

}
