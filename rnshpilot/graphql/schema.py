import graphene

from rnshpilot import settings
from rnshpilot.utils import openehr_utils


class AllergiesType(graphene.ObjectType):
    name = graphene.String(description='The name of the Allergy the patient has')
    date = graphene.String(description='Then date the patient identified the allergy')


class PatientType(graphene.ObjectType):
    id = graphene.Int(description='openEHR Party Id of the Patient')
    mrn = graphene.String(description='Medical Record Number used for patient identification at RNSH')
    ehrId = graphene.String(description='openEHR electronic health record identifier')
    dob = graphene.String(description='Patient Date of birth')
    firstname = graphene.String(description='Patient first name')
    surname = graphene.String(description='Patient surname')
    address = graphene.String(description='Patients main contact address')
    phone = graphene.String(description='Patients phone number')
    email = graphene.String(description='Patients email address')
    gender = graphene.String(description='Patient Gender, either MALE or FEMALE')
    tumorType = graphene.String(description='Tumour Type Either Prostate, Breast or CNS')
    surgical = graphene.String(description='If a patient has had surgery on their tumour then true otherwise false')
    allergies = graphene.List(of_type=AllergiesType, description='A list of allergies that the patient may have')

    def resolve_ehr_id(self, args, context, info):
        url = 'ehr/?subjectId={}&subjectNamespace={}'.format(
           self.mrn, settings.OPEN_EHR_SUBJECT_NAMESPACE
        )
        resp = openehr_utils.get(url)
        return resp['ehrId']


class MessageInput(graphene.InputObjectType):
    message = graphene.String(required=True)


class Query(graphene.ObjectType):
    patients = graphene.List(PatientType)
    patient = graphene.Field(PatientType, id=graphene.Int())
    echo = graphene.String(description='Echo what you enter', message=graphene.String())

    def resolve_patients(self, args, context, info):
        url = 'demographics/party/query/?lastNames=*&rnsh.mrn=*'
        resp = openehr_utils.get(url)

        patients = []
        for party in resp['parties']:
            patient = openehr_utils.party_to_patient(party)
            patients.append(patient)

        return patients

    def resolve_patient(self, args, context, info):
        url = 'demographics/party/{}'.format(args.get('id'))
        resp = openehr_utils.get(url)

        return openehr_utils.party_to_patient(resp['party'])

    def resolve_echo(self, args, context, info):
        return args.get('message')


schema = graphene.Schema(query=Query)
