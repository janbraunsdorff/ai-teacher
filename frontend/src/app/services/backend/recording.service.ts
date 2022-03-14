import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {environment} from '../../../environments/environment'
import { JwtHelperService } from "@auth0/angular-jwt";

@Injectable({
  providedIn: 'root'
})
export class RecordingService {
  private helper;


  constructor(private client: HttpClient) { 
    this.helper = new JwtHelperService();

  }



  sendWav(blob: Blob, title: string) {
    let token = localStorage.getItem('token') 
    const decodedToken = this.helper.decodeToken(token!);
    title = decodedToken.sub + '_' + title

    let formData = new FormData();
    formData.append('wave', blob);    
    formData.append('data', title)
    this.client.post(environment.host + '/recording/save', formData).subscribe(res => {
      console.log(res)
    }, (err) => {
      console.log(err)
    })
  }


  getTexts() {
    return this.client.get(environment.host + '/recording/text')
  }
}
