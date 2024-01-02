from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_patient, name='search_patient'),
]