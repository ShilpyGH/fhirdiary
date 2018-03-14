import { TestBed, inject } from '@angular/core/testing';

import { GenerateService } from './generate.service';

describe('GenerateService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [GenerateService]
    });
  });

  it('should be created', inject([GenerateService], (service: GenerateService) => {
    expect(service).toBeTruthy();
  }));
});
