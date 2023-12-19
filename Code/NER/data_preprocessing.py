# MIT licensed
import os
from transformers import AutoTokenizer
import numpy as np
import datasets
import matplotlib.pyplot as plt

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')


OG_DATA_DIR = 'cadec/original/'
TXT_DATA_DIR = 'cadec/text/'

ENTITIES = ['O','B-adr', 'B-disease', 'B-drug', 'B-symptom', 'B-finding',
         'I-adr', 'I-disease', 'I-drug', 'I-symptom', 'I-finding']

def remove_duplicates(labels, positions):
    """Removes duplicate labels and positions combinations."""

    new_labels, new_positions = [], []
    for label, position in zip(labels, positions):

        if (label, position) not in zip(new_labels, new_positions):
            new_labels.append(label)
            new_positions.append(position)

    return new_labels, new_positions


def extract_data(ann_data):
    """Extracts the labels and positions from the .ann file.

    Input text:
    T1	ADR 88 94	cramps
    T2	ADR 99 121	heavy vaginal bleeding
    #1	AnnotatorNotes T2	But this could possibly be describing menorrhagia
    T3	ADR 126 132;175 182	period another
    T4	Symptom 17 21	pain
    T1	Drug 246 263	voltaren rapid 25

    Returns:
    labels =    ['ADR',     'ADR',      'ADR',      'ADR',      'Symptom'   ]
    positions = [(88, 94),  (99, 121),  (126, 132), (175, 182), (17, 21)    ]
    """
    
    labels = []
    positions = []

    for line in ann_data:

        if line.startswith('T'):
            
            line = line.replace(';', ' ')
            line = line.split()

            for i in range(2, len(line), 2):
                if line[i].isnumeric():
                    positions.append((int(line[i]), int(line[i+1])))
                    labels.append(line[1])
                else:
                    break
    
    return labels, positions


def annotate_text(labels, positions, txt_data):
    """Annotates the text with the labels.

    Input text:
    labels =    ['Symptom', 'ADR',      'ADR',      'ADR',      'ADR'       ]
    positions = [(17, 21),  (88, 94),   (99, 121),  (126, 132), (175, 182)  ] SORTED FROM LOWEST TO HIGHEST
    Didn't have much pain relief, and within a few days of starting the meds I began having cramps and heavy vaginal bleeding.
    My period ended last week and this med made me have another one!.

    Returns:
    Didn't have much <Symptom> pain </Symptom> relief, and within a few days of starting the meds I began having <ADR> cramps </ADR> and <ADR> heavy vaginal bleeding </ADR>.
    My <ADR> period </ADR> ended last week and this med made me have <ADR> another </ADR> one!.
    """

    offset = 0
    ann_txt = txt_data
    for label, position in zip(labels, positions):
        start, end = position
        start += offset
        end += offset
        ann_txt = ann_txt[:start] + f'<{label}> ' + ann_txt[start:end] + f' </{label}>' + ann_txt[end:]
        offset += 2*len(label) + 7
    
    return ann_txt


def annotated_text_to_iob(ann_text):
    """Converts the annotated text to IOB format.

        Input text with labels:
        Didn't have much <Symptom> pain </Symptom> relief, and within a few days of starting the meds I began having <ADR> cramps </ADR> and <ADR> heavy vaginal bleeding </ADR>.
        My <ADR> period </ADR> ended last week and this med made me have <ADR> another </ADR> one!.

        Returns:
        Annotated text in IOB format.
    """
    tokenizer.add_tokens(['<Symptom>', '</Symptom>', '<ADR>', '</ADR>', '<Drug>', '</Drug>',
                          '<Disease>', '</Disease>', '<Finding>', '</Finding>'])
    tokenized_txt = tokenizer.tokenize(ann_text)
    iob = []
    entity = "O"
    for token in tokenized_txt:
        if token.startswith('</') and token.endswith('>'):
            entity = "O"
            continue
        elif token.startswith('<') and token.endswith('>'):
            entity = 'B-'+token[1:-1]
            continue
        else:
            iob.append((token, entity))
            entity = 'I-'+entity[2:] if entity != 'O' else 'O'
    return iob


def apply_preprocessing(ann_data, txt_data):
    """Applies the preprocessing to the data."""

    labels, positions = extract_data(ann_data)
    labels, positions = remove_duplicates(labels, positions)
    labels, positions = zip(*sorted(zip(labels, positions), key=lambda x: x[1][0]))

    ann_txt = annotate_text(labels, positions, txt_data)

    iob = annotated_text_to_iob(ann_txt)

    return iob


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


# def read_data():
#     """Reads the .ann and .txt files and processes the data into iob format."""

#     file_names = os.listdir(OG_DATA_DIR)
#     file_names = [file[:-4] for file in file_names]
    
#     drug_names = get_random_split(file_names)

#     raw_datasets = {'train':        {'id': [], 'tokens': [], 'ner_tags': []},
#                     'validation':   {'id': [], 'tokens': [], 'ner_tags': []},
#                     'test':         {'id': [], 'tokens': [], 'ner_tags': []}}
    
#     for file in file_names:

#         name = file.split('.')[0]
#         number = int(file.split('.')[1])
#         dataset = 'train' if number in drug_names[name]['train'] else \
#                     'validation' if number in drug_names[name]['validation'] else 'test'
        
#         with open(OG_DATA_DIR + file + '.ann', 'r') as f, open(TXT_DATA_DIR + file + '.txt', 'r') as f2:
#             ann_data = f.readlines()
#             if len(ann_data) == 0:
#                 continue
#             txt_data = f2.readlines()
#             txt_data = ' '.join([line.strip() for line in txt_data])

#             iob = apply_preprocessing(ann_data, txt_data)

#             raw_datasets[dataset]['tokens'].append([token for token, _ in iob])
#             raw_datasets[dataset]['ner_tags'].append([tag for _, tag in iob])
    
#     for dataset in raw_datasets:
#         raw_datasets[dataset]['id'] = [i for i in range(len(raw_datasets[dataset]['tokens']))]
#         raw_datasets[dataset] = datasets.Dataset.from_dict(raw_datasets[dataset])
#     raw_datasets = datasets.DatasetDict(raw_datasets)
#     raw_datasets.save_to_disk('cadec/processed')

    # return raw_datasets


def process_data():

    txt_lengts = []

    file_names = os.listdir(OG_DATA_DIR)
    file_names = [file[:-4] for file in file_names]

    drug_names = get_random_split(file_names)

    with open('cadec/processed/train.ann', 'w') as f_train, \
         open('cadec/processed/valid.ann', 'w') as f_valid, \
         open('cadec/processed/test.ann', 'w') as f_test:

        for file in file_names:

            name = file.split('.')[0]
            number = int(file.split('.')[1])
            
            if number in drug_names[name]['train']:
                f = f_train
            elif number in drug_names[name]['validation']:
                f = f_valid
            else:
                f = f_test

            with open(OG_DATA_DIR + file + '.ann', 'r') as f1, open(TXT_DATA_DIR + file + '.txt', 'r') as f2:
                ann_data = f1.readlines()
                if len(ann_data) == 0:
                    continue
                txt_data = f2.readlines()
                txt_data = ' '.join([line.strip() for line in txt_data])

                iob = apply_preprocessing(ann_data, txt_data)
                txt_lengts.append(len(iob))
                if len(iob) > 512:
                    print(file, len(iob))

                for token, tag in iob:
                    f.write(f'{token}\t{tag}\n')
                f.write('\n')

    # plt.hist(txt_lengts, bins=50)
    # plt.show()

if __name__ == "__main__":
    process_data()
