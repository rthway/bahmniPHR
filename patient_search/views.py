from django.shortcuts import render
from .utils import get_patient_data

def search_patient(request):
    if request.method == 'POST':
        identifier = request.POST.get('patient_identifier', '')
        patient_data = get_patient_data(identifier)

        return render(request, 'patient_search/search_result.html', {'patient_data': patient_data})

    return render(request, 'patient_search/search_patient.html')
