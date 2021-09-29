from django.urls import path
#from rest_framework import routers
from .views import PropertiesList, valid_smiles_view, PharmacophoreList

#from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register('properties', PropertiesList)

#urlpatterns = router.urls

urlpatterns = [
    path('properties/', PropertiesList.as_view()),
    path('validation/', valid_smiles_view),
    path('pharmacophores/', PharmacophoreList.as_view())
]