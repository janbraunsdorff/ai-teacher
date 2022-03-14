import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageSegementationComponent } from './image-segementation.component';

describe('ImageSegementationComponent', () => {
  let component: ImageSegementationComponent;
  let fixture: ComponentFixture<ImageSegementationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImageSegementationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageSegementationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
