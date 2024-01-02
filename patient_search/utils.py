import requests
from datetime import datetime
import json
import urllib3
urllib3.disable_warnings()

"""
disable_warnings()
import urllib3
urllib3.disable_warnings()
"""



def get_patient_data(identifier):
    api_url = "https://192.168.2.40/openmrs/ws/rest/v1/bahmnicore/search/patient/lucene"

    # Set the authentication credentials
    auth = ("superman", "Admin123")

    # Define the parameters for the API request
    params = {
        "addressFieldName": "city_village",
        "addressSearchResultsConfig": ["city_village", "address1"],
        "filterOnAllIdentifiers": False,
        "identifier": identifier,
        "loginLocationUuid": "e6f6e53c-637a-4166-966c-94c24b852965",
        "programAttributeFieldValue": "",
        "s": "byIdOrNameOrVillage",
        "startIndex": 0
    }

    try:
        # Make the API request with authentication
        response = requests.get(api_url, params=params, auth=auth, verify=False)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Parse and print the obtained data
        data = response.json()

        if 'pageOfResults' in data and data['pageOfResults']:
            patient = data['pageOfResults'][0]

            # Extracting relevant information
            fullname = f"{patient.get('givenName', '')} {patient.get('middleName', '')} {patient.get('familyName', '')}"

            # Parsing the 'addressFieldValue' JSON-encoded string
            address_field_value = json.loads(patient.get('addressFieldValue', '{}'))
            municipality = address_field_value.get('city_village', '')
            ward = address_field_value.get('address1', '')

            gender = patient.get('gender', '')

            # Calculating age from birth date
            birth_date = datetime.strptime(patient.get('birthDate', ''), '%Y-%m-%d')
            today = datetime.now()
            age = (today - birth_date).days // 365

            person_id = patient.get('personId', '')
            patient_identifier = patient.get('identifier', '')
            uuid = patient.get('uuid','')

            # Print the extracted information
            # print("Extracted Data:")
            # print(f"Person ID: {uuid}")
            # print(f"Patient Identifier: {patient_identifier}")
            # print(f"Person ID: {person_id}")
            # print(f"Fullname: {fullname}")
            # print(f"Municipality: {municipality}")
            # print(f"Ward: {ward}")
            # print(f"Gender: {gender}")
            # print(f"DOB: {age} years")

            # return
            return {
            'uuid': uuid,
            'identifier': patient_identifier,
            'fullname': fullname,
            'municipality': municipality,
            'ward': ward,
            'gender': gender,
            'age': age,
        }



        else:
            print("No patient data found for the given identifier.")

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")


if __name__ == "__main__":
    # Get user input for the patient identifier
    user_identifier = input("Enter patient identifier: ")

    # Call the function with the user-provided identifier
    get_patient_data(user_identifier)

