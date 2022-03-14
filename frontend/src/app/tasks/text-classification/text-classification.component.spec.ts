import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TextClassificationComponent } from './text-classification.component';

describe('TextClassificationComponent', () => {
  let component: TextClassificationComponent;
  let fixture: ComponentFixture<TextClassificationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TextClassificationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TextClassificationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
