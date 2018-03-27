USER_IDS = {'Julie Margaret Doe': 'cf-1519578984350',
           'Jane Doe': 'cf-1519579101695'}

USER_INFO = {
    'Jane Doe':
        {
            'user_type': 'relatedperson',
            'active': True,
             'address': [{'city': 'Salt Lake City',
               'line': ['123 Some Place'],
               'postalCode': '84103',
               'state': 'UT'}],
             'birthDate': '1975-07-06',
             'gender': 'female',
             'id': 'cf-1519579101695',
             'identifier': [{'value': 'RelPer-1'}],
             'meta': {'lastUpdated': '2018-02-26T20:53:56.000+00:00', 'versionId': '1'},
             'name': [{'family': 'Doe', 'given': ['Jane']}],
             'patient': {'reference': 'Patient/cf-1519578984350'},
             'relationship': {'coding': [{'code': 'MTH',
                'display': 'mother',
                'system': 'http://hl7.org/fhir/v3/RoleCode'}]},
             'resourceType': 'RelatedPerson',
             'telecom': [{'system': 'phone', 'use': 'home', 'value': '801-123-4567'}],
             'text': {'div': '<div xmlns="http://www.w3.org/1999/xhtml"><a name="mm"></a></div>',
              'status': 'generated'
            }
        },
    'Julie Margartet Doe' :  {
             'user_type': 'patient',
             'address': [{'city': 'Salt Lake City',
             'line': ['123 Some Place'],
             'postalCode': '84103',
             'state': 'UT'}],
             'birthDate': '2005-05-04',
             'gender': 'female',
             'id': 'cf-1519578984350',
             'identifier': [{'value': 'Pat-1'}],
             'meta': {'lastUpdated': '2018-02-26T20:53:56.000+00:00', 'versionId': '1'},
             'name': [{'family': 'Doe', 'given': ['Julie', 'Margaret']}],
             'resourceType': 'Patient',
             'telecom': [{'system': 'phone', 'use': 'home', 'value': '801-123-4567'}],
             'text': {'div': '<div xmlns="http://www.w3.org/1999/xhtml"><a name="mm"></a></div>',
              'status': 'generated'
        }
    }
}


USER_RELATS = {
    'Jane Doe': {
        'patient': 'Julie Margaret Doe',
        'relationship': 'mother'
        }
    }


TRIGGER_CODES = {
    'Sleep deprivation': '130989002',
     'Increased stress': '23085004',
    'Photosensitivity': '90128006',
}

HEADACHE_CODE = '25064002'
