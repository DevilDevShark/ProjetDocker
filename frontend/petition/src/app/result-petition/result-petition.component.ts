import { Component, OnInit } from '@angular/core';

import { DataService } from './../services/data.service';

@Component({
  selector: 'app-result-petition',
  templateUrl: './result-petition.component.html',
  styleUrls: ['./result-petition.component.css']
})
export class ResultPetitionComponent implements OnInit {

  items: any[] = [];

  constructor(private dataService: DataService) { }

  ngOnInit() {
    this.dataService.getPetitions()
      .subscribe((petitions) => {
        console.log(petitions);
        this.items = petitions;
      });
  }

}
