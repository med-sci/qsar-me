from mapex.geneticAlgorithm import GA
from mapex.pharmacophore import PharmComplex
from mapex.models import ModelProperties


obf = ModelProperties.objects.get(id=1)
smiles = obf.smiles.split(',')
ga = GA(obf.id, smiles, 3, obf.num_inds, obf.mutation_chance, 3)
ga.run()
mols = ga.get_molecules()
chromosome = ga.best_chromosome
p = PharmComplex(mols, chromosome)
p.create()
coords = p.get_coords()
print(coords)

#exec(open('mapex/ga_script.py').read())

