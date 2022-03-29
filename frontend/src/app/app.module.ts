import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LayoutComponent } from './common/layout/layout.component';
import { LabelingLayoutComponent } from './common/labeling-layout/labeling-layout.component';
import {MatCheckboxModule} from '@angular/material/checkbox';


import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatNativeDateModule} from '@angular/material/core';
import {HttpClientModule, HTTP_INTERCEPTORS} from '@angular/common/http';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatListModule} from '@angular/material/list';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import {MatInputModule} from '@angular/material/input';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatChipsModule} from '@angular/material/chips';
import {MatStepperModule} from '@angular/material/stepper';
import {MatSelectModule} from '@angular/material/select';
import {MatDialogModule} from '@angular/material/dialog';
import {MatTabsModule} from '@angular/material/tabs';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';



import { LandingPageComponent } from './common/landing-page/landing-page.component';
import { ImageSegementationComponent } from './tasks/image-segementation/image-segementation.component';
import { CanvasComponent } from './common/canvas/canvas.component';
import { ImageClassificationComponent } from './tasks/image-classification/image-classification.component';
import { SubmitComponent } from './common/submit/submit.component';
import { ImageExtractionComponent } from './tasks/image-extraction/image-extraction.component';
import { ImageSegExtComponent } from './tasks/image-seg-ext/image-seg-ext.component';
import { TextClassificationComponent } from './tasks/text-classification/text-classification.component';
import { TextEntityRegistrationComponent } from './tasks/text-entity-registration/text-entity-registration.component';
import { AudioRecordingComponent } from './tasks/audio-recording/audio-recording.component';
import { AudioValidationComponent } from './tasks/audio-validation/audio-validation.component';
import { TextComponent } from './common/text/text.component';
import { LandingComponent } from './user/landing/landing.component';
import { InterceptorService } from './guard/interceptor.service';
import { CreateProjectComponent } from './project/create-project/create-project.component';
import { ProjectMetaComponent } from './project/project-meta/project-meta.component';
import { ProjectComponent } from './project/project/project.component';
import { TasksComponent } from './project/project/tasks/tasks.component';
import { DataComponent } from './project/project/data/data.component';
import { StatsComponent } from './project/project/stats/stats.component';
import { DataImageComponent } from './project/project/data/data-image/data-image.component';
import { ImageDetailsComponent } from './project/project/data/data-image/image-details/image-details.component';
import { WorkerComponent } from './project/project/worker/worker.component';
import { WorkerDetailComponent } from './project/project/worker/worker-detail/worker-detail.component';
import { TeachComponent } from './project/project/teach/teach.component';
import { ClassesComponent } from './project/project/classes/classes.component';
import { DataAudioTextComponent } from './project/project/data/data-audio-text/data-audio-text.component';
import { ClassComponent } from './project/project/classes/class/class.component';




@NgModule({
  declarations: [
    AppComponent,
    LayoutComponent,
    LabelingLayoutComponent,
    LandingPageComponent,
    ImageSegementationComponent,
    CanvasComponent,
    ImageClassificationComponent,
    SubmitComponent,
    ImageExtractionComponent,
    ImageSegExtComponent,
    TextClassificationComponent,
    TextEntityRegistrationComponent,
    AudioRecordingComponent,
    AudioValidationComponent,
    TextComponent,
    LandingComponent,
    CreateProjectComponent,
    ProjectMetaComponent,
    ProjectComponent,
    TasksComponent,
    DataComponent,
    StatsComponent,
    DataImageComponent,
    ImageDetailsComponent,
    WorkerComponent,
    WorkerDetailComponent,
    TeachComponent,
    ClassesComponent,
    DataAudioTextComponent,
    ClassComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    MatNativeDateModule,
    ReactiveFormsModule,
    MatSidenavModule,
    MatListModule,
    MatToolbarModule,
    MatIconModule,
    MatCheckboxModule,
    MatInputModule,
    MatExpansionModule,
    MatChipsModule,
    MatStepperModule,
    MatSelectModule,
    MatDialogModule,
    MatTabsModule,
    MatProgressBarModule,
    MatSlideToggleModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: InterceptorService, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
