import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AudioService {

  public textRecording = new Subject<AudioRecording>();

  constructor(private client: HttpClient) { }

  getNextAudioRecodring(pid: string) {
    this.client.get<AudioRecording>(environment.host + '/audio/' + pid + '/next-recording').subscribe(res => {
      this.textRecording.next(res)
    }, err => {
      console.log(err);
    })
  }

  saveAudio(pid: string, blob: Blob, text_id: string) {
    let formData = new FormData();
    formData.append('wave', blob);    
    formData.append('text_id', text_id)
    this.client.post(environment.host + '/audio/' + pid + '/save-record', formData).subscribe(res => {
      console.log(res)
      this.getNextAudioRecodring(pid)
    }, (err) => {
      console.log(err)
    })
  }
}


export interface AudioRecording {
  id: string
  text: string
}