import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreatePetitionComponent } from './create-petition/create-petition.component';
import { ResultPetitionComponent } from './result-petition/result-petition.component';
import { VotePetitionComponent } from './vote-petition/vote-petition.component';

const routes: Routes = [
  { path: 'create-petition-component', component: CreatePetitionComponent },
  { path: 'result-petition-component', component: ResultPetitionComponent },
  { path: 'vote-petition-component', component: VotePetitionComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
