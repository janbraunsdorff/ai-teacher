import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LandingPageComponent } from './common/landing-page/landing-page.component';
import { AuthGuardService } from './guard/auth-guard.service';
import { ClassesComponent } from './project/project/classes/classes.component';
import { DataComponent } from './project/project/data/data.component';
import { ProjectComponent } from './project/project/project.component';
import { StatsComponent } from './project/project/stats/stats.component';
import { TasksComponent } from './project/project/tasks/tasks.component';
import { TeachComponent } from './project/project/teach/teach.component';
import { WorkerComponent } from './project/project/worker/worker.component';
import { AudioRecordingComponent } from './tasks/audio-recording/audio-recording.component';
import { AudioValidationComponent } from './tasks/audio-validation/audio-validation.component';
import { ImageClassificationComponent } from './tasks/image-classification/image-classification.component';
import { ImageExtractionComponent } from './tasks/image-extraction/image-extraction.component';
import { ImageSegExtComponent } from './tasks/image-seg-ext/image-seg-ext.component';
import { ImageSegementationComponent } from './tasks/image-segementation/image-segementation.component';
import { TextClassificationComponent } from './tasks/text-classification/text-classification.component';
import { TextEntityRegistrationComponent } from './tasks/text-entity-registration/text-entity-registration.component';
import { LandingComponent } from './user/landing/landing.component';

const routes: Routes = [
  {path: '', pathMatch: 'full', component: LandingPageComponent, canActivate: [AuthGuardService]},
  {path: 'login', component: LandingComponent},
  {path: 'start', canActivate: [AuthGuardService], canActivateChild: [AuthGuardService], component: LandingPageComponent},
  {path: 'teach/:id', canActivate: [AuthGuardService], canActivateChild: [AuthGuardService], children: [
    {path: 'img-bounding-box', component: ImageSegementationComponent},
    {path: 'img-classification', component: ImageClassificationComponent},
    {path: 'img-extraction', component: ImageExtractionComponent},
    {path: 'segmentation-extraction', component: ImageSegExtComponent},
    {path: 'recording', component: AudioRecordingComponent},
    {path: 'validation', component: AudioValidationComponent},
    {path: 'text-extraction', component: TextEntityRegistrationComponent},
  ]},
  {path: 'text', canActivate: [AuthGuardService], canActivateChild: [AuthGuardService], children: [
    {path: 'classification', component: TextClassificationComponent},
    {path: 'recognition', component: TextEntityRegistrationComponent}
  ]},
  {path: 'project', canActivate: [AuthGuardService], canActivateChild: [AuthGuardService], children: [
    {path: ':id', component: ProjectComponent, children: [
      {path: 'tasks', component: TasksComponent},
      {path: 'data', component: DataComponent},
      {path: 'stats', component: StatsComponent},
      {path: 'worker', component: WorkerComponent},
      {path: 'teach', component: TeachComponent},
      {path: 'classes', component: ClassesComponent},
    ]}
  ]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
