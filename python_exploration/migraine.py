from datetime import datetime
import random
from dateutil.relativedelta import relativedelta
now = datetime.now()
from collections import Counter

import matplotlib.pyplot as plt

# Import modules and classes for working with FHIR resources
from fhirclient import client
import json
from fhirclient.models.relatedperson import RelatedPerson
from fhirclient.models.patient import Patient
from fhirclient.models.condition import Condition
from fhirclient.models.observation import Observation
from fhirclient.models.medicationadministration import MedicationAdministration
from fhirclient.models.medicationrequest import MedicationRequest
from fhirclient.models.list import List


from migraine_data import *

def get_user(username, usertype, server):
    if usertype == 'patient':
        user =  Patient.read(USER_IDS[username], server)
    elif usertype == 'care partner':
        user = RelatedPerson.read(USER_IDS[username], server)
    elif usertype == 'clinician':
        raise NotImplementedError

    return user

def display_user(user):
    usertype = 'Patient' if isinstance(user, Patient) else 'Care Partner'
    name = "{} {}".format(' '.join(user.name[0].given), user.name[0].family)

    dob = datetime.strptime(user.birthDate.isostring, '%Y-%m-%d')
    gender = user.gender
    addr = user.address[0]
    addr = "{} {} {} {}".format(addr.line[0],  addr.city,  addr.state, addr.postalCode)
    print(usertype.upper())
    print('----------------------')
    print("Name: {}".format(name))
    print("Gender: {}".format(gender))
    print("DOB: {}".format(dob))
    print("Address: {}".format(addr))
    if usertype == 'Care Partner':
        print('Relationship: Mother to [Julie Margaret Doe]')
    return


def get_pain_levels(patient_name, server):
    search = Observation.where({
                            "subject": 'Patient/{}'.format(
                                USER_IDS[patient_name]),
                             'code': 'LA25253-8'})
    pain_levels = search.perform_resources(server)

#     search = Observation.where({'subject': data_dict['patient_ref'],
#                                'code': data_dict['pain_sev_code']})
#     observations = search.perform_resources(smart.server)

    return pain_levels

def sort_resources_by_date(resources):
    resources.sort(key=lambda x:x.effectiveDateTime.date)
    return resources


def display_pain_levels(pain_levels):
    pain_levels = sort_resources_by_date(pain_levels)
    for pain in pain_levels:
        print('{}: {}/10'.format(
            pain.effectiveDateTime.date.strftime("%M-%d-%Y"),
            pain.valueQuantity.value,))


def plot_pain_levels(patient_name, server):
    pain_levels = get_pain_levels(patient_name, server)
    pain_levels = sort_resources_by_date(pain_levels)
    x = range(len(pain_levels))
    x_labels = [pain.effectiveDateTime.date.strftime("%M-%d-%Y") for pain in pain_levels]
    x_labels

    y = [pain.valueQuantity.value for pain in pain_levels]


    plt.plot(x, y, marker='.')
    plt.title("{}'s migraine pain levels".format(patient_name))

    _ = plt.xticks(x, x_labels, rotation=45)


def get_triggers(patient_name, server):
    triggers = []
    for trig_code in TRIGGER_CODES.values():
        search = Condition.where({
                            "subject": 'Patient/{}'.format(
                                USER_IDS[patient_name]),
                                'code': trig_code
        })
        triggers.extend(search.perform_resources(server))
        # DUMMY EXAMPLE TO HAVE ONE EXTRA
        if trig_code == '130989002':
            triggers.extend(search.perform_resources(server))
    return triggers



def plot_triggers(patient_name, server):
    trigs = get_triggers(patient_name, server)
    trig_names = [trig.code.coding[0].display for trig in trigs]
    trig_names.sort()
    counter = Counter(trig_names)
    x_labels, y = zip(*counter.items())
    x = range(len(y))
    plt.title("{}'s headache triggers".format(patient_name))
    plt.bar(x, y)
    plt.xticks(x, x_labels)


def get_active_medications(patient_name, server):

    search = MedicationRequest.where({'subject': 'Patient/{}'.format(
                                USER_IDS[patient_name]),
                                   'status': 'active'})
    med_requests = search.perform_resources(server)
    return med_requests


def display_medication_list(patient_name, server):
    meds = get_active_medications(patient_name, server)
    med_display = ['{} - {}'.format(med.medicationCodeableConcept.coding[0].display,
                                    med.dosageInstruction[0].text)
                          for med in meds]
    med_display.sort()
    for i, med in enumerate(med_display):
        print('{}.  {}'.format(i+1, med))



# Code for creating new resources
def create_fhir_list(entry):
    # 1. Transform Headache into a Condition
    # Let's transform our entry into a new dictionary
    entry_dict = {}

    # Add an id
    id_num = random.choice(range(1000000)) # Does this matter?
    entry_dict['id'] = 'cf-{}'.format(id_num)
    dt = '{}T{}:00.000Z'.format(entry['date'], entry['time'])
    entry_dict['date'] = dt


    # Add these other attributes, some of which I don't fully understand
    id_num = random.choice(range(10000))

    entry_dict.update(
        {'identifier': [{'value': 'List-{}'.format(id_num)}],
         'meta': {'lastUpdated': dt, 'versionId': '1'},
         'mode': 'snapshot',
         'resourceType': 'List',
         'status': 'current',
         'text': {'div': '<div xmlns="http://www.w3.org/1999/xhtml"><a name="mm"></a></div>',
          'status': 'generated'}}
    )

    # Now create the conditions and observations

    # Add the subject
    author = entry['author']
    author_id = USER_IDS[author]
    if USER_INFO[author] == 'patient':
        subject_id = {
           'reference': 'Patient/{}'.format((USER_IDS[author]))
        }
    else:
       subject_id = {
           'reference': 'Patient/{}'.format((USER_IDS[USER_RELATS[author]['patient']]))
        }


    # A list of all new resources, including our List
    resources = []
    # References to other resources in our List
    entry_refs = []

    # Create new resources from the entry items
    # Start with headache
    headache_entry = entry['entries']['headache'][0]
    new_resource = create_condition(headache_entry, 'headache', author_id, subject_id)
    resources.append(new_resource)
    entry_refs.append({'item': {'reference': '{}/{}'.format(
            new_resource.as_json()['resourceType'], new_resource.as_json()['id'])
    }})

    # Now pain severity
    new_resource = create_pain_severity(headache_entry, author_id, subject_id)
    resources.append(new_resource)
    entry_refs.append({'item': {'reference': '{}/{}'.format(
            new_resource.as_json()['resourceType'], new_resource.as_json()['id'])
    }})

    # Now triggers
    for trigger_entry in entry['entries']['triggers']:

        new_resource = create_condition(trigger_entry, 'trigger', author_id, subject_id)
        resources.append(new_resource)
        entry_refs.append(
            {'item': {'reference': '{}/{}'.format(
            new_resource.as_json()['resourceType'], new_resource.as_json()['id'])
                                   }})

    # TODO: Medications


    # Add references to our other resources
    entry_dict['entry'] = entry_refs

    # Create a new List resource
    fhir_list = List(entry_dict)
    resources.append(fhir_list)
    return resources


def create_condition(entry, entry_type, author_id, subject_id):
    cond_dict = {}

    if author_id == subject_id: # This means it's a patient doing the asserting
        author_type = 'Patient'
    else:
        author_type = 'RelatedPerson'
    cond_dict['asserter'] = {'reference': '{}/{}'.format(author_type, author_id)}
    cond_dict['subject'] = {'reference': 'Patient/{}'.format(subject_id)}

    cond_dict['clinicalStatus'] = 'active'

    # Add coding
    code_dict = {'system': 'http://snomed.info/sct'}
    if entry_type == 'trigger':
        code_dict['code'] = TRIGGER_CODES[entry['name']]
        code_dict['display'] = entry['name']
    elif entry_type == 'headache':
        code_dict['code'] = HEADACHE_CODE
        code_dict['display'] = 'Headache'


    cond_dict['code'] = {'coding': [code_dict]}

    dt = '{}T{}:00.000Z'.format(entry['date'], entry['time'])
    cond_dict['onsetDateTime'] = dt

    cond_dict['resourceType'] = 'Condition'

    id_num = random.choice(range(10000))
    cond_dict['id'] = 'cf-{}'.format(id_num)

    cond_dict['identifier'] = [{'value': '{}-{}'.format(entry_type, id_num)}]

    cond_dict['text'] = {
        'div': '<div xmlns="http://www.w3.org/1999/xhtml"><a name="mm"></a></div>',
        'status': 'generated'
    }
    cond_dict['verificationStatus']: 'confirmed'

    trig = Condition(cond_dict)
    return trig


def create_pain_severity(entry, author_id, subject_id):
    obs_dict = {}

    # Add an id
    id_num = random.choice(range(1000000)) # Does this range matter?
    obs_dict['id'] = 'cf-{}'.format(id_num)

    # Required arguments
    obs_dict['status'] = 'active'
    obs_dict['code'] =  {'coding': [{'code': 'LA25253-8', 'display': 'Pain severity 0-10',
                         'system': 'http://loinc.org'}]}
    obs_dict


    # Instead of 'asserter', this resource has 'performer'
    # 'performer': [{'reference': 'Patient/cf-1519578984350'}],

    if author_id == subject_id: # This means it's a patient doing the asserting
        author_type = 'Patient'
    else:
        author_type = 'RelatedPerson'

    obs_dict['performer'] = [{'reference': '{}/{}'.format(author_type, author_id)}]
    obs_dict['subject'] = {'reference': 'Patient/{}'.format(subject_id)}


    # Set the effectiveDateTime
    # Same as the other one
    dt = '{}T{}:00.000Z'.format(entry['date'], entry['time'])
    obs_dict['effectiveDateTime'] = dt

    #coding': [{'code': 'LA25253-8', 'display': 'Pain severity 0-10', 'system': 'http://loinc.org'}]},
    obs_dict['valueQuantity'] = {'value':  int(entry['severity'])}
    obs = Observation(obs_dict)
    return obs
