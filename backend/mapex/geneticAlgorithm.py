from django.core.files import File
from django.core.files.storage import default_storage
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors, PyMol, SDWriter
from rdkit.six import StringIO
import random
from loguru import logger
from statistics import stdev
from statistics import mean
from pathlib import Path



class GA:
    def __init__(
        self, model_id, 
        smiles,  n_conformers, n_inds, 
        mutation_chance,
        generations, 
        crippen=False, 
        verbose = True, 
        ):
        self._model_id = model_id
        self._smiles = smiles
        self._nconfs = n_conformers
        self._mols = self._create_confs()
        self._MMFFs = self._MMFF_props
        self._Crippens = self._crippen_contribs
        self._ref = self._mols[0]
        self._prbs = self._mols[1:]
        self._n_inds = n_inds
        self._population = self.__population
        self._mut_chance = mutation_chance
        self._num_gens = generations
        self._useCrippen = crippen
        self._cache = []
        self.population = []
        self.best_chromosome = None
        self.verbose = verbose

    def _create_confs(self):
        mols = []
        for smile in self._smiles:
            m = Chem.MolFromSmiles(smile)
            m = AllChem.AddHs(m)
            c = AllChem.EmbedMultipleConfs(m, self._nconfs)
            mols.append(AllChem.RemoveHs(m))
        return mols

    class _Chromosome:
        def __init__(self, n_confs, n_genes):
            self._n_confs = n_confs
            self._n_genes = n_genes
            self.score = None
            self.chromosome = self._chromosome

        def __repr__(self):
            return "chromosome"

        @property
        def _chromosome(self):
            chromosome = [
                random.randint(0, self._n_confs - 1) for _ in range(self._n_genes)
            ]
            return chromosome

    def _cache_population(self, population):
        for chromosome in population:
            if chromosome.chromosome not in self._cache:
                self._cache.append(chromosome.chromosome)
        return self._cache

    @property
    def _MMFF_props(self):
        return [AllChem.MMFFGetMoleculeProperties(m) for m in self._mols]

    @property
    def _crippen_contribs(self):
        return [rdMolDescriptors._CalcCrippenContribs(m) for m in self._mols]

    @property
    def __population(self):
        return [
            self._Chromosome(self._mols[0].GetNumConformers(), len(self._mols))
            for _ in range(self._n_inds)
        ]

    def __fitness(self, chromosome):
        if chromosome.chromosome in self._cache:
            return chromosome
        else:
            ref = self._ref
            prbs = self._prbs
            scores = []
            for i in range(len(prbs)):
                if self._useCrippen:
                    o3a = AllChem.GetCrippenO3A(
                        prbs[i],
                        ref,
                        self._crippen_contribs[i + 1],
                        self._crippen_contribs[0],
                        prbCid=chromosome.chromosome[i + 1],
                        refCid=chromosome.chromosome[0],
                    )
                else:
                    o3a = AllChem.GetO3A(
                        prbs[i],
                        ref,
                        self._MMFFs[i + 1],
                        self._MMFFs[0],
                        prbCid=chromosome.chromosome[i + 1],
                        refCid=chromosome.chromosome[0],
                    )
                rmsd = o3a.Align()
                matches = o3a.Matches()
                score = (len(matches) / ref.GetNumAtoms()) * 100 + min(
                    (rmsd / 0.04) * 100, 100
                )
                scores.append(score)
            total = round((mean(scores) - stdev(scores)), 2)
            chromosome.score = total
            return chromosome

    @staticmethod
    def __order_population(population):
        return sorted(population, key=lambda chromosome: chromosome.score, reverse=True)

    @staticmethod
    def __crossover(population):
        splt = random.randint(1, len(population[0].chromosome) - 1)
        if len(population) % 2 == 0:
            len_pop = len(population) - 1
        else:
            len_pop = len(population)
        for i in range(1, len_pop, 2):
            children1 = (
                population[i].chromosome[0:splt] + population[i + 1].chromosome[splt:]
            )
            children2 = (
                population[i + 1].chromosome[0:splt] + population[i].chromosome[splt:]
            )
            population[i].chromosome = children1
            population[i + 1].chromosome = children2
        return population

    @staticmethod
    def __mutation(chromosome, chance):
        assert chance > 0 and chance <= 1
        distribution = [chance, 1 - chance]
        random_number = random.choices([1, 0], distribution)
        if random_number[0] == 1:
            gene = random.randint(0, len(chromosome.chromosome) - 1)
            chromosome.chromosome[gene] = random.randint(0, chromosome._n_confs - 1)
        return chromosome

    def run(self):
        population = self._population
        for _ in range(self._num_gens):
            population = [self.__fitness(chromosome) for chromosome in population]
            population = self.__order_population(population)
            self._cache_population(population)
            if self.verbose:
                logger.info(f'Chromosome with score {population[0].score} created')
            population = self.__crossover(population)
            population = [population[0]] + [
                self.__mutation(chromosome, self._mut_chance)
                for chromosome in population[1:]
            ]
        population = [self.__fitness(chromosome) for chromosome in population]
        population = self.__order_population(population)
        if self.verbose:
            logger.info(f'chromosome with score {population[0].score} created')
        self.population = population
        self.best_chromosome = population[0].chromosome

    def get_molecules(self):
        ref = self._ref
        prbs = self._prbs
        chromosome = self.best_chromosome
        for i, mol in enumerate(prbs):
            o3a = AllChem.GetO3A(
                mol,
                ref,
                self._MMFFs[i+1],
                self._MMFFs[0],
                prbCid=chromosome[i + 1],
                refCid=chromosome[0],
            )
            o3a.Align()
        mols = [ref] + prbs
        return mols

    @staticmethod
    def write(molecules, chromosome, model_id):
        sio = StringIO()
        with SDWriter(sio) as w:
            for m, g in zip(molecules, chromosome):
                w.write(m, confId=g)
        file = default_storage.open(f'molecules_{model_id}.sdf', 'w')
        file.write(sio.getvalue())
        file.close()

        
        
        
    
