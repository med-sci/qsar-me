from django.db import models
from django.db.models import fields
from rest_framework.fields import ReadOnlyField
from .models import ModelProperties, Pharmacophore
from rest_framework.serializers import ModelSerializer, ValidationError
from rdkit import Chem


class PropertiesSerializer(ModelSerializer):
    class Meta:
        model = ModelProperties
        fields = [
            'id', 
            'smiles',
            'num_inds',
            'num_confs',
            'mutation_chance',
            'generations',
            'use_crippen',
            'email'
        ]
    def validate_smiles(self, value):
        smiles = value.split(',') # reusable code  :(
        mols = [Chem.MolFromSmiles(smile) for smile in smiles]
        if None in  mols:
            raise ValidationError('Incorrect smile in list')
        else:
            return value


class PharmacophoreSerializer(ModelSerializer):
    class Meta:
        model = Pharmacophore
        fields = [
            'id',
            'model', 
            'label',
            'x',
            'y',
            'z'
        ]