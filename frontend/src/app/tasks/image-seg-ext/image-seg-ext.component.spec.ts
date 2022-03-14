import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageSegExtComponent } from './image-seg-ext.component';

describe('ImageSegExtComponent', () => {
  let component: ImageSegExtComponent;
  let fixture: ComponentFixture<ImageSegExtComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImageSegExtComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageSegExtComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
