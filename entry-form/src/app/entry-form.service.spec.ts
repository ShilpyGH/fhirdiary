import { TestBed, inject } from '@angular/core/testing';

import { EntryFormService } from './entry-form.service';

describe('EntryFormService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [EntryFormService]
    });
  });

  it('should be created', inject([EntryFormService], (service: EntryFormService) => {
    expect(service).toBeTruthy();
  }));
});
