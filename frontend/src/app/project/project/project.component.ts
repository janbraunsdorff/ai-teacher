import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import {map} from 'rxjs/operators';

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.scss']
})
export class ProjectComponent implements OnInit {
  links = [
    {path: 'stats', name: 'Statistics'},
    {path: 'teach', name: 'Teach'},
    {path: 'worker', name: 'Worker'},
    {path: 'data', name: 'Data'},
    {path: 'tasks', name: 'Tasks'},
    {path: 'classes', name: 'Classes'},
  ];

  activeLink = ''
  project_id = ''

  constructor(private currentRoute: ActivatedRoute, private router: Router) { }

  ngOnInit(): void {
    this.currentRoute.url.pipe(map( seg => {
      return seg[0].path
    })).subscribe((id) => {
      this.project_id = id
    })

    this.router.events.subscribe((val) => {
      if (val instanceof NavigationEnd) {
        this.activeLink = val.url.split('/').reverse()[0]
      }
    })

    this.activeLink = this.router.url.split('/').reverse()[0]
      
  }

}
