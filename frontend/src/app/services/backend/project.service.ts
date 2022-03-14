import { HttpClient, HttpEventType } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
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

    uploadData(file: File, projectId: string, kind: string) {
      const body = new FormData()
      body.append('kind', kind)
      body.append('file', file)
      this.client.post(environment.host + "/project/"+ projectId +"/data", body, {reportProgress: true, observe: 'events'})
      .subscribe((res) => {
        if (res.type === HttpEventType.UploadProgress) {
          const percentDone = Math.round(100 * res.loaded / res.total!);
          this.progess.next(percentDone)
        }else if (res.type === HttpEventType.Response){
          setTimeout(() => {
            this.progess.next(null)
          }, 1000);

          this.getImageData(projectId)
          this.getAudioTextData(projectId)
        }
      }, (err) => {
        this.progess.next(null)
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

    add_class(pid: string, name: string, desc: string) {
      this.client.post(environment.host + '/project/' + pid + '/classes', {name: name, description: desc}).subscribe(res =>{
        this.get_classes(pid)
      })
    }


    get_classes(pid: string) {
      this.client.get<Class[]>(environment.host + '/project/' + pid + '/classes').subscribe(res => {
        this.classes.next(res)
      }, err => {
        console.log(err)
      })
    }


    deleteClass(pid: string, cid: string) {
      this.client.delete(environment.host + '/project/' + pid + '/classes', {body: {class_id: cid}}).subscribe(res => {
        this.get_classes(pid)
      }, err => {
        console.log(err)
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
  worker_id: string,
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