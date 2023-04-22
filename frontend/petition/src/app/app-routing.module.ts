import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ResultPetitionComponent } from './result-petition/result-petition.component';

const routes: Routes = [
  { path: '', component: ResultPetitionComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
