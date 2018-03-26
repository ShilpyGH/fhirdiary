# Import modules and classes for working with FHIR resources
from fhirclient import client
from fhirclient.models.relatedperson import RelatedPerson
from fhirclient.models.patient import Patient
from fhirclient.models.condition import Condition
from fhirclient.models.observation import Observation
from fhirclient.models.medicationadministration import MedicationAdministration
from fhirclient.models.medicationrequest import MedicationRequest

import matplotlib.pyplot as plt


from datetime import datetime
from dateutil.relativedelta import relativedelta
now = datetime.now()


USER_IDS = {'Julie Margaret Doe': 'cf-1519578984350',
           'Jane Doe': 'cf-1519579101695'}

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
