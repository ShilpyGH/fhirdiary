import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { catchError, map, tap } from 'rxjs/operators';

import { Injectable } from '@angular/core';
import { MessageService } from './message.service';

import { Entry } from './entry'

import { HttpClient, HttpHeaders } from '@angular/common/http';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable()
export class EntryFormService {

  private entriesUrl = 'api/entries';

  constructor(
    private http: HttpClient,
    private messageService: MessageService
  ) { }

  private log(message: string) {
    console.log("In log");
    console.log(message);
    // TODO: Add the message service if needed
    this.messageService.add('EntryFormService: ' + message);
    console.log(this.messageService);
  }

  // TODO: Define getEntries()
  // ...

  getEntries() {
    this.messageService.add("fetched entries");
  }

  /** POST: add a new entry to the server */
  addEntry (entry: Entry): Observable<Entry> {
    let response = this.http.post<Entry>(this.entriesUrl,
      entry, httpOptions).pipe(
        // TODO: Figure out why this isn't working
        tap( (entry: Entry) => this.log('Added entry {entry.id}')),
      )
    console.log(this.messageService);
    return response
  }


}
