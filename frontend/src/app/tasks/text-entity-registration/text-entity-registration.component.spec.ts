import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TextEntityRegistrationComponent } from './text-entity-registration.component';

describe('TextEntityRegistrationComponent', () => {
  let component: TextEntityRegistrationComponent;
  let fixture: ComponentFixture<TextEntityRegistrationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TextEntityRegistrationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TextEntityRegistrationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
