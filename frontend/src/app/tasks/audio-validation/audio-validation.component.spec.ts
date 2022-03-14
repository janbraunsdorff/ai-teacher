import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AudioValidationComponent } from './audio-validation.component';

describe('AudioValidationComponent', () => {
  let component: AudioValidationComponent;
  let fixture: ComponentFixture<AudioValidationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AudioValidationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AudioValidationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
