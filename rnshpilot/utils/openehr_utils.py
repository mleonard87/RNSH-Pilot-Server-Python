import requests

from requests.auth import HTTPBasicAuth

from rnshpilot import settings


def get(url_suffix):
    auth = HTTPBasicAuth(settings.OPEN_EHR_USERNAME, settings.OPEN_EHR_PASSWORD)
    url = '{}{}'.format(settings.OPEN_EHR_BASE_URL, url_suffix)
    resp = requests.get(url, auth=auth)

    return resp.json()


def flatten_additional_party_info(additional_party_info):
    flattened = {}
    for info in additional_party_info:
        flattened[info['key']] = info['value']

    return flattened


def party_to_patient(party_json):
    from rnshpilot.graphql.schema import PatientType, AllergiesType
    additional_party_info = flatten_additional_party_info(party_json['partyAdditionalInfo']);
    new_patient = PatientType(
        id=party_json['id'],
        mrn=additional_party_info['rnsh.mrn'],
        ehrId=party_json.get('id', ''),
        dob=party_json['dateOfBirth'],
        firstname=party_json['firstNames'],
        surname=party_json['lastNames'],
        address=party_json['address']['address'],
        phone=additional_party_info['phone'],
        email=additional_party_info['email'],
        gender=party_json['gender'],
        tumorType=additional_party_info['tumorType'],
        surgical=additional_party_info['surgical'],
        allergies=[
            AllergiesType(name='Insulin', date='2005-07-16'),
            AllergiesType(name='Penicillin', date='2005-07-16'),
            AllergiesType(name='Dust', date='1982-03-21'),
            AllergiesType(name='Latex', date='1986-11-02'),
        ],
    )
    return new_patient
