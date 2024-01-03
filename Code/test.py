import os
import numpy as np

def get_random_split(file_names):
    """
    Split the data into train, validation and test sets, while making sure 
    each drug is represented in each set.
    """

    train_split, valid_split = 0.8, 0.1

    drug_names = {}
    for file_name in file_names:
        drug_name = file_name.split('.')[0]
        if drug_name not in drug_names:
            drug_names[drug_name] = 1
        else:
            drug_names[drug_name] += 1
    
    for drug_name in drug_names:
        indices = np.arange(drug_names[drug_name])
        np.random.shuffle(indices)
        drug_names[drug_name] = indices
        train, validation, test = np.split(indices, [int(train_split*len(indices)), int((train_split+valid_split)*len(indices))])

        drug_names[drug_name] = {'train': train, 'validation': validation, 'test': test}
    
    return drug_names

if __name__ == "__main__":
    OG_DATA_DIR = 'cadec/original/'
    file_names = os.listdir(OG_DATA_DIR)
    file_names = [file[:-4] for file in file_names]

    drug_names = get_random_split(file_names)
