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
  import_data = {
    path: ""
  }
  
  constructor(private currentRoute: ActivatedRoute, private service: ProjectService) { }

  ngOnInit(): void {
    this.currentRoute.parent?.params.subscribe((val) => {
      this.project_id = val['id']
    })
  }


  import(){
    if (this.import_data.path != "") {
      this.service.postImport(this.import_data, this.project_id)
      this.import_data.path = ""
    }
  }

}
