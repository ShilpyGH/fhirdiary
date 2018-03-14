export class BaseEntryField {

  fullDate: Date;
  date: String;
  time: String;

  constructor() {
    let fullDate = new Date();
    this.date = this.setDefaultDate();
    this.time = this.setDefaultTime();
  }

  setDefaultDate() {

    let dateString = '';
    let fullDate = new Date();
    dateString += fullDate.getFullYear() + '-';


    let m = fullDate.getMonth();
    if (m < 10) {
      dateString += '0' + m.toString() + '-';
    }
    else {
      dateString += m.toString() + '-';
    }
    let d = fullDate.getDate();
    if (d < 10) {
      dateString += '0' + d.toString();
    }
    else {
      dateString += d.toString();
    }
    return dateString;
  }

  /**
  Returns a string format of the current time
  %H-%M
  */
  setDefaultTime() {
    let fullDate = new Date();
    let h = fullDate.getHours();
    let hourString = '';
    if (h < 10)
      hourString += '0' + h.toString() + ':';
    else
      hourString += h.toString() + ':'

    let m = fullDate.getMinutes();
    if (m < 10)
      hourString += '0' + m.toString();
    else
      hourString += m.toString();

    return hourString;


  }
}

/**
Class that represents an entire entry.
*/
class Entry extends BaseEntryField {


  entryFields: EntryField; // An interface

  constructor() {
    super();

    // TODO: Is there a better way to do this? Maybe it should have its own class or interface
    this.entryFields = {
                      // TODO: author should be set some other way
                      'author': "Mrs. Julia's Mom",
                      'headache': null, // TODO: change this to null
                      'medications': [],
                      'triggers': [],
                      'comments': ''
    }


  }
}


class HeadacheEntry extends BaseEntryField {
  severity: number;
  idx?: number;

  constructor() {
    super();
    this.severity = 0;


  }
}

class MedicationEntry extends BaseEntryField {

  name: String;
  idx?: number;

  constructor(name: String) {
    super();
    this.name = name;
  }
}

class TriggerEntry extends BaseEntryField {

  name: String;
  idx?: number;
  constructor(name: String) {
    super();
    this.name = name;
  }
}

interface EntryField {
  author: string;
  headache?: HeadacheEntry;
  triggers?: TriggerEntry[];
  medications?: MedicationEntry[];
  comments: string;
}


export { Entry, TriggerEntry, MedicationEntry, HeadacheEntry }
