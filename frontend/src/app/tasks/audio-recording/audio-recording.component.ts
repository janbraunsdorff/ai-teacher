import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { RecordedAudioOutput, RecordService } from 'src/app/services/audio/record.service';
import { AudioRecording, AudioService } from 'src/app/services/backend/audio.service';
import { RecordingService } from 'src/app/services/backend/recording.service';

@Component({
  selector: 'app-audio-recording',
  templateUrl: './audio-recording.component.html',
  styleUrls: ['./audio-recording.component.scss']
})
export class AudioRecordingComponent implements OnInit, OnDestroy {
  private subText: Subscription|null = null
  public state = "ready"
  public text: AudioRecording|null = null
  pid = ''
  public record: null| RecordedAudioOutput = null

  constructor(private recService: RecordService, public backend: AudioService, private currentRoute: ActivatedRoute) { }
  
  ngOnDestroy(): void {
    if (this.subText != null) {
      this.subText.unsubscribe()
    }
  }
  

  ngOnInit(): void {
    this.recService.getRecordedBlob().subscribe((data) => {
      this.record = data
      this.state = "done"
    })

    this.subText = this.backend.textRecording.subscribe((data) => {
      this.text = data
    })

    this.currentRoute.parent?.params.subscribe((val) => {
      this.pid = val['id']
      this.backend.getNextAudioRecodring(this.pid)
    })
  }

  public changeState(state: string) {
    this.state = state;
  }
  

  @HostListener('document:keypress', ['$event'])
  handleKeyboardEvent(event: KeyboardEvent) { 
    if (this.text == null) {
      return
    }
    let key: string = event.key + this.state;
    
    if (key === ' ') {
      console.log('ready for recording')
      this.state = "ready"
    }

    if (key === ' ready') {
      console.log('start recoding')
      this.recService.startRecording();
      this.state = "hear"; 
    }

    if (key === ' hear') {
      console.log('stop recoding')
      this.recService.stopRecording(this.text?.id);
    }

    if (key === 'Enterdone' && this.record != null) {
      console.log('send ...')
      this.backend.saveAudio(this.pid, this.record.blob, this.text.id)
      this.state = "ready"      
    }

    if (key == 'rdone' && this.record != null) {
      this.record = null
      this.state = "ready"
      console.log('retry')
    }
  }
}
