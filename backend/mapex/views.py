from statistics import mode
from django.http import Http404, request
from numpy import result_type
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from .serializers import PropertiesSerializer, PharmacophoreSerializer, ResultSerializer
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


class PharmacophoreDetail(generics.ListAPIView):
    serializer_class = PharmacophoreSerializer

    def get_queryset(self):
        queryset = Pharmacophore.objects.all()
        model_id = self.request.query_params.get('model')
        if model_id is not None:
            queryset = queryset.filter(model=model_id)
        return queryset


class ResultList(APIView):

    def get(self, request):
        results = ResultModel.objects.all()
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

class ResultDetail(APIView):

    def get_object(self, pk):
        try:
            return ResultModel.objects.get(pk=pk)
        except ResultModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        result = self.get_object(pk)
        serializer = ResultSerializer(result)
        return Response(serializer.data)