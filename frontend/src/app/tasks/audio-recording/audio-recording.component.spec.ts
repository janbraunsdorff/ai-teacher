import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AudioRecordingComponent } from './audio-recording.component';

describe('AudioRecordingComponent', () => {
  let component: AudioRecordingComponent;
  let fixture: ComponentFixture<AudioRecordingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AudioRecordingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AudioRecordingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
