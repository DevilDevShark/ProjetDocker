import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';


@Component({
  selector: 'app-create-petition',
  templateUrl: './create-petition.component.html',
  styleUrls: ['./create-petition.component.css']
})
export class CreatePetitionComponent implements OnInit {

  public petitionForm:FormGroup;
  titre: string = "";
  desc: string = "";
  constructor( private fb: FormBuilder) {
    this.petitionForm = this.fb.group({
      titre: '',
      desc: ''
    });
  }


  setValue() {
    this.titre=this.petitionForm.get('titre')?.value;
    this.desc=this.petitionForm.get('desc')?.value;
  }

  ngOnInit(): void {
  }
}
