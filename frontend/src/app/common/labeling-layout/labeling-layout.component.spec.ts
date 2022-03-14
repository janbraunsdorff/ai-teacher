import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelingLayoutComponent } from './labeling-layout.component';

describe('LabelingLayoutComponent', () => {
  let component: LabelingLayoutComponent;
  let fixture: ComponentFixture<LabelingLayoutComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LabelingLayoutComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LabelingLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
