import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Segement } from 'src/app/models/datatypes';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ImageService {
  public classes = new Subject<NextImage>();
  public bouding = new Subject<NextImage>();
  public extraction = new Subject<NextImage>();

  constructor(private client: HttpClient) { }

  getNextClassification(pid: string) {
    this.client.get<NextImage>(environment.host + '/images/' + pid + '/next-class').subscribe(res => {
      this.classes.next(res)
    }, err => {
      console.log(err);
    })
  }

  classify(pid: string, iid:string, cid: string){
    this.client.post(environment.host + '/images/' + pid + '/classify', {iid, cid}).subscribe(res => {
      console.log(res)
    }, err => {
      console.log(err)
    })
  }

  boundingbox(pid: string, label_id: string, image_id: string, segments: Segement, value: string|undefined){
    if (segments == undefined) {
      return
    }
    this.client.post(environment.host + '/images/' + pid + '/bounding', {label_id, image_id, segments, value}).subscribe(res => {
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

  extract(pid: string, img_id: string, class_id: string, value: string ){
    if (value == undefined || value == '') { return }
    this.client.post(environment.host + '/images/' + pid + '/extraction', {img_id, class_id, value}).subscribe(res => {
    }, err => {
      console.log(err)
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
  id: string,
  name: string,
  desc: string,
}


export interface NextImage{
  id: string
  width: number
  height: number
  classes: Class[]
}