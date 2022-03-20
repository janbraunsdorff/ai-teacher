import { HttpClient, HttpEventType } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Subject, throwError } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
    public projects = new Subject<Project[]>();
    public progess = new Subject<number | null>();
    public images = new Subject<ImageMeta[]>();
    public tasks = new Subject<Task[]>();
    public worker = new Subject<Labler[]>();
    public classes = new Subject<Class[]>();
    public excercies = new Subject<Excercie[]>();
    public audio = new Subject<AudioTextMeta[]>();
    public import = new Subject<ImportResult>();
    
    constructor(private client: HttpClient) { }

    createProject(name: string) {
      this.client.post(environment.host + "/project/create", {name})
      .subscribe((res) => {
        this.getProjects()
      }, (err) => {
        console.log(err)
      });
    }

    getProjects() {
      this.client.get<Project[]>(environment.host + "/project/all")
      .subscribe( (res) => {
        console.log(res)
        this.projects.next(res)
      }, (err) => {
        console.log(err)
      })
    }

    postImport(data: any, projectId: string) {
      return this.client.post<ImportResult>(environment.host + "/project/"+ projectId +"/import", data).subscribe(
        (res) => {
          this.import.next(res)
          this.getImageData(projectId)
        },(err) => {
          console.log(err)
        })
    }

    getImageData(projectId: string) {
      return this.client.get<ImageMeta[]>(environment.host + "/project/"+ projectId +"/images")
      .subscribe(res => {
        this.images.next(res)
      })
    }


    getAudioTextData(projectId: string) {
      return this.client.get<AudioTextMeta[]>(environment.host + "/project/"+ projectId +"/audio-text")
      .subscribe(res => {
        console.log(res);
        
        this.audio.next(res)
      })
    }

    

    getProjectTasks(projectId: string){
      this.client.get<Task[]>(environment.host + '/project/' + projectId + '/tasks').subscribe((res) => {
        this.tasks.next(res)
      })
    }

    toggle(project_id: string, task_id: string) {
      this.client.post<Task[]>(environment.host + '/project/' + project_id + '/toggle-task', {task_id}).subscribe((res) => {
        this.getProjectTasks(project_id)
      })
    }

    getWorker(projectId: string) {
      this.client.get<Labler[]>(environment.host + "/project/" + projectId + "/worker").subscribe((res) => {
        this.worker.next(res)
      })
    }

    toggleWorker(project_id: string, worker_id: string){
      this.client.post(environment.host + '/project/' + project_id + '/toggle-worker', {worker_id}).subscribe((res) => {
        this.getWorker(project_id)
      })
    }


    getExcercies(pid: string){
      this.client.get<Excercie[]>(environment.host + '/project/' + pid + '/teach').subscribe(res => {
        this.excercies.next(res)
      }, err => {
        console.log(err)
      })
    }
    

}

export interface AudioTextMeta {
  text: string
  id: string,
  tasks: TaskShort[]

}

export interface Project {
  id: string,
  name: string,
  created: string
}

export interface ImageMeta {
  name: string,
  shape: string,
  tasks: TaskShort[]
}

export interface TaskShort {
  name: string,
  done: boolean
}

export interface Task{
  name: string,
  id: string,
  type: string,
  selected: boolean
}

export interface Labler {
  name: string,
  id: string,
  alias: string,
  is_worker: string
}


export interface Class {
    class_id: string,
    name: string,
    description: string,
    connected_points: number
}

export interface Excercie {
  task_id: string,
  task_name: string,
  processed: number,
  total: number,
  data_type: string
}

export interface ImportResult {
  num_imported: number
  error_files: string[]
}