import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VotePetitionComponent } from './vote-petition.component';

describe('VotePetitionComponent', () => {
  let component: VotePetitionComponent;
  let fixture: ComponentFixture<VotePetitionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VotePetitionComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VotePetitionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
