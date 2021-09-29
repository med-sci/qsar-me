from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from .serializers import PropertiesSerializer, PharmacophoreSerializer
from .validators import validate_smiles
from .tasks import run_ga


# Create your views here.
@api_view(['POST'])
def valid_smiles_view(request):
    smiles = request.data['smiles']
    status = ''
    try:
        validate_smiles(smiles)
        status = 'OK'
    except ValueError:
        status = 'ERROR'
    return Response({'status':status})


class PropertiesList(APIView):

    def get(self, request):
        properties = ModelProperties.objects.all()
        serializer = PropertiesSerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PropertiesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            run_ga(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PharmacophoreList(APIView):

    def get(self, request):
        properties = Pharmacophore.objects.all()
        serializer = PharmacophoreSerializer(properties, many=True)
        return Response(serializer.data)