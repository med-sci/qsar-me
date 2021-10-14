from qsarme.celery import app
from mapex.geneticAlgorithm import GA
from mapex.models import ModelProperties, Pharmacophore, ResultModel
from mapex.pharmacophore import PharmComplex 
from .service import send
from loguru import logger


@app.task
def run_ga(id):
    logger.info('Starting genetic algorithm.')
    obj = ModelProperties.objects.get(id=id)
    smiles = obj.smiles.split(',')
    logger.info('Building molecule conformations')
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
    logger.info('Writing molecules..')
    ga.write(mols, chromosome, ga._model_id)
    link = f'https://mapex-test.s3.amazonaws.com/molecules_{obj.id}.sdf' #add to env
    logger.info('Building Pharmacophore')
    p = PharmComplex(mols, chromosome)
    p.create(distance=obj.distance)
    coords = p.get_coords()
    for key,value in coords.items():
        if value != []:
            for coord in value:
                pharmacophore = Pharmacophore(
                    model=obj, 
                    label=key, 
                    x=coord[0],
                    y=coord[1],
                    z=coord[2])
                pharmacophore.save()
    result = ResultModel(model = obj, s3_url=link)
    result.save()
    logger.info('Sending email..')
    url = f'http://localhost:8080/report/{obj.id}'
    send(obj.email, url)
    logger.info('Done!')
    
    