import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataAudioTextComponent } from './data-audio-text.component';

describe('DataAudioTextComponent', () => {
  let component: DataAudioTextComponent;
  let fixture: ComponentFixture<DataAudioTextComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DataAudioTextComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataAudioTextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
