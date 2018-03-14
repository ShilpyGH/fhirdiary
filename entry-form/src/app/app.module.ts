import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';


import { AppComponent } from './app.component';
import { EntryFormComponent } from './entry-form/entry-form.component';
// import { GenerateService } from './generate.service';


@NgModule({
  declarations: [
    AppComponent,
    EntryFormComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
  ],
  providers: [],
  // providers: [GenerateService],
  bootstrap: [AppComponent]
})
export class AppModule { }
