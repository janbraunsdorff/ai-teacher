import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageExtractionComponent } from './image-extraction.component';

describe('ImageExtractionComponent', () => {
  let component: ImageExtractionComponent;
  let fixture: ComponentFixture<ImageExtractionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImageExtractionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageExtractionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
