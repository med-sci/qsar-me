from django.urls import path
from .views import (
    PharmacophoreDetail,
    PropertiesList, 
    ResultDetail, 
    valid_smiles_view, 
    ResultList)

urlpatterns = [
    path('properties/', PropertiesList.as_view()),
    path('validation/', valid_smiles_view),
    path('pharmacophores/', PharmacophoreDetail.as_view()),
    path('results/', ResultList.as_view()),
    path('results/<int:pk>', ResultDetail.as_view())
]