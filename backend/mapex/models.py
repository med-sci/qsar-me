from django.db import models
from django.db.models.deletion import CASCADE
from .validators import validate_smiles

# Create your models here.


class ModelProperties(models.Model):
    smiles = models.TextField(max_length=1000, validators=[validate_smiles])
    num_inds = models.IntegerField()
    num_confs = models.IntegerField(default=50)
    mutation_chance = models.FloatField()
    generations = models.IntegerField()
    use_crippen = models.BooleanField(default=False)
    email = models.EmailField()
    link = models.URLField()

    def __str__(self):
        return f'model-{self.pk}'

class Pharmacophore(models.Model):
    model = models.ForeignKey(ModelProperties, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()





