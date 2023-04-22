import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CreatePetitionComponent } from './create-petition.component';

describe('CreatePetitionComponent', () => {
  let component: CreatePetitionComponent;
  let fixture: ComponentFixture<CreatePetitionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreatePetitionComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreatePetitionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
