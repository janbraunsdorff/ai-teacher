import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Segement } from 'src/app/models/datatypes';
import { environment } from 'src/environments/environment';
import { ImageMeta, ProjectService } from './project.service';

@Injectable({
  providedIn: 'root'
})
export class ImageService {
  public classes = new Subject<NextImage>();
  public bouding = new Subject<NextImage>();
  public extraction = new Subject<NextImage>();

  constructor(private client: HttpClient, private project_service: ProjectService) { }

  getNextClassification(pid: string) {
    this.client.get<NextImage>(environment.host + '/images/' + pid + '/next-class').subscribe(res => {
      this.classes.next(res)
      console.log(res)
    }, err => {
      console.log(err);
    })
  }

  classify(pid: string, iid:string, cid: string){
    this.client.post(environment.host + '/images/' + pid + '/classify', {"document_id": iid, "class_name": cid}).subscribe(res => {
      console.log(res)
    }, err => {
      console.log(err)
    })
  }

  boundingbox(pid: string, image_id: string, segments: Segement, value: string|undefined){
    if (segments == undefined) {
      return
    }
    this.client.post(environment.host + '/images/' + pid + '/bounding', {image_id, segments, value}).subscribe(res => {
    }, err => {
      console.log(err)
    })
  }

  getNextBoudingBox(pid: string) {
    this.client.get<NextImage>(environment.host + '/images/' + pid + '/next-bounding').subscribe(res => {
      this.bouding.next(res)
    }, err => {
      console.log(err);
    })
  }

  extract(pid: string, payload: any){
    this.client.post(environment.host + '/images/' + pid + '/extract', payload).subscribe(res => {
      console.log(res)
      this.getNextExtraction(pid)
    }, err => {
      console.log(err)
    })
  }

  relabel(projectId: string, docId: string, type: string) {
    return this.client.get<ImageMeta[]>(environment.host + "/images/"+ projectId + "/" + type + "/" + docId)
      .subscribe(() => {
        this.project_service.getImageData(projectId)
      })
  }

  getNextExtraction(pid: string) {
    this.client.get<NextImage>(environment.host + '/images/' + pid + '/next-extraction').subscribe(res => {
      this.extraction.next(res)
    }, err => {
      console.log(err);
    })
  }
}


export interface Class{
  name: string,
  desc: string,
}


export interface NextImage{
  id: string
  width: number
  height: number
  classes: Class[]
}