from mapex.geneticAlgorithm import GA
from mapex.models import ModelProperties
from mapex.pharmacophore import PharmComplex 

def run_ga(id):
    obj = ModelProperties.objects.get(id=id)
    smiles = obj.smiles.split(',')
    ga = GA(
        obj.id, 
        smiles, 
        obj.num_confs, 
        obj.num_inds, 
        obj.mutation_chance, 
        obj.generations)
    ga.run()
    mols = ga.get_molecules()
    chromosome = ga.best_chromosome
    ga.write(mols, chromosome, ga._model_id)
    obj.link = f'https://mapex-test.s3.amazonaws.com/molecules_{obj.id}.sdf'
    p = PharmComplex(mols, chromosome)
    pharmacophore = p.create()
    
    