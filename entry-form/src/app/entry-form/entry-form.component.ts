import { Component, OnInit } from '@angular/core';

import { Entry, MedicationEntry, TriggerEntry,  HeadacheEntry } from '../entry';


@Component({
  selector: 'app-entry-form',
  templateUrl: './entry-form.component.html',
  styleUrls: ['./entry-form.component.css']
})


export class EntryFormComponent implements OnInit {

  // Hardcoded values for triggers and meds
  TRIGGER_VALUES = ['Air Quality', 'Lack of Sleep',
              'Food', 'Light'];
  MEDICATION_VALUES = ['Ibuprofen 200mg', 'Tylenol 100mg'];


  model: Entry;
  submitted: boolean;

  newHeadache: HeadacheEntry;
  newTrigger: TriggerEntry;
  newMedication: MedicationEntry;

  constructor() {
    this.model = new Entry();
    this.submitted = false;
    // Entries in progress
    this.newHeadache = new HeadacheEntry();
    this.newTrigger = new TriggerEntry("Air Quality");
    this.newMedication = new MedicationEntry("Ibuprofen 200mg")
   }

  ngOnInit() { }

  // // getEntries() {
  //   this.entries = this.entryFormService.getEntries();
  // }

  hasTrigger() {
    return this.model.entryFields.triggers.length > 0;
  }

  hasHeadache() {
    return this.model.entryFields.headache.length > 0;
  }

  getTriggerValues() {
    return this.TRIGGER_VALUES;
  }

  addNewHeadache() {
    // Copy the object that I've been called 'newHeadache'
    let newHeadache = Object.assign({},  this.newHeadache);
    this.model.entryFields.headache = [newHeadache];
  }

  removeHeadache() {
    this.model.entryFields.headache = [];
  }


  /**
  Adds the `newTrigger` field to the Entry's current triggers
  */
  addNewTrigger() {
    this.newTrigger.idx = this.model.entryFields['triggers'].length;
    let newTrigger = Object.assign({}, this.newTrigger);
    this.model.entryFields['triggers'].push(newTrigger);
    this.newTrigger = new TriggerEntry('Air Quality');
  }

  /**
  Removes the trigger from entryFields.triggers at idx
  */
  removeTrigger(idx) {
    // Remove the previous trigger
    this.model.entryFields['triggers'].splice(idx, 1);

    // Now change idxs in the remaining trigger entries
    for (let i = idx; i<this.model.entryFields.triggers.length; i++) {
      this.model.entryFields.triggers[i].idx = i;
    }
  }

  addNewMedication() {
    this.newMedication.idx = this.model.entryFields['medications'].length;
    let newMed = Object.assign({}, this.newMedication);
    this.model.entryFields['medications'].push(newMed);
    this.newMedication = new MedicationEntry('Ibuprofen 200mg');
  }

  removeMedication(idx) {
    this.model.entryFields['medications'].splice(idx, 1);
    // Now change idxs in the remaining trigger entries
    for (let i = idx; i<this.model.entryFields.medications.length; i++) {
      this.model.entryFields.medications[i].idx = i;
    }
  }



  onSubmit() {
    this.submitted = true;

    console.log("Will submit. We'll figure out what to do here.");
    console.log(this.model);
  }

  get diagnostic() {return JSON.stringify(this.model);}



}
