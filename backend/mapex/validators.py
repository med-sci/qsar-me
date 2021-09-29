from rdkit import Chem


def validate_smiles(value):
    if value == '':
        raise ValueError
    smiles = value.split(',') # handle exc
    mols = [Chem.MolFromSmiles(smile) for smile in smiles]
    if None in  mols:
        raise ValueError('Incorrect smile in list') #ПОЧЕМУ ОШИБКА ИЗ ДЖАНГИ НЕ ПЕРЕХВАТЫВАЕТСЯ??