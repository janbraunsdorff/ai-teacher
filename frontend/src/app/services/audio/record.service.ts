import { Injectable } from '@angular/core';
import * as RecordRTC from 'recordrtc';
import { Observable, Subject } from 'rxjs';


export interface RecordedAudioOutput {
  blob: Blob;
  title: string;
}

@Injectable({
  providedIn: 'root'
})
export class RecordService {
  private stream: any;
  private recorder: any;
  private interval: any;
  private startTime: any;
  private _recorded = new Subject<RecordedAudioOutput>();
  private _recordingTime = new Subject<string>();
  private _recordingFailed = new Subject<string>();


  getRecordedBlob(): Observable<RecordedAudioOutput> {
    return this._recorded.asObservable();
  }

  getRecordedTime(): Observable<string> {
    return this._recordingTime.asObservable();
  }

  recordingFailed(): Observable<string> {
    return this._recordingFailed.asObservable();
  }


  startRecording() {
    if (this.recorder) {
      return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(s => {
        this.stream = s;
        this.record();
      }).catch(error => {
        this._recordingFailed.next(error);
      });

  }

  abortRecording() {
    this.stopMedia();
  }

  private record() {

    this.recorder = new RecordRTC.StereoAudioRecorder(this.stream, {
      type: 'audio',
      mimeType: 'audio/wav',
      desiredSampRate: 16000,
      //disableLogs: false,
      //timeSlice: 1000,
      //audioBitsPerSecond: 128000,
      sampleRate: 48000,
      //ufferSize: 16384,
      numberOfAudioChannels: 1,
    });
    console.log('init recorder done')

    this.recorder.record();
  }

  stopRecording(id: string) {
    if (this.recorder) {
      this.recorder.stop((blob: any) => {
          this.stopMedia();
          this._recorded.next({ blob: blob, title: id + '.wav' });
      }, () => {
        this.stopMedia();
        this._recordingFailed.next();
      });
    }
  }

  private stopMedia() {
    if (this.recorder) {
      this.recorder = null;
      clearInterval(this.interval);
      this.startTime = null;
      if (this.stream) {
        this.stream.getAudioTracks().forEach((track: any) => track.stop());
        this.stream = null;
      }
    }
  }

}
