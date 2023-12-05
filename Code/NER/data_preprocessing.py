# MIT licensed
import os


OG_DATA_DIR = 'cadec/original/'
TXT_DATA_DIR = 'cadec/text/'

ENTITIES = ['O'
            'B-ADR', 'B-Disease', 'B-Drug', 'B-Symptom', 'B-Finding',
            'I-ADR', 'I-Disease', 'I-Drug', 'I-Symptom', 'I-Finding']


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
    positions = ['88, 94),  (99, 121),  (126, 132), (175, 182), (17, 21)    ]
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
    labels =    ['ADR',     'ADR',      'ADR',      'ADR',      'Symptom'   ]
    positions = ['88, 94),  (99, 121),  (126, 132), (175, 182), (17, 21)    ]
    Didn't have much pain relief, and within a few days of starting the meds I began having cramps and heavy vaginal bleeding.
    My period ended last week and this med made me have another one!.

    Returns:
    Didn't have much <Symptom> pain </Symptom> relief, and within a few days of starting the meds I began having <ADR> cramps </ADR> and <ADR> heavy vaginal bleeding </ADR>.
    My <ADR> period </ADR> ended last week and this med made me have <ADR> another </ADR> one!.
    """
    
    return


def annotated_text_to_iob(ann_text):
    """Converts the annotated text to IOB format.

        Input text:
        <ADR> Side effect name </ADR> <Drug> Drug name </Drug> <Disease> Disease name </Disease> 
        <Symptom> Symptom name </Symptom> <Finding> Finding name </Finding>.

        Returns:
        [('side', 'B-ADR'), 
        ('effect', 'I-ADR'), 
        ('name', 'I-ADR'), 
        ('drug', 'B-Drug'), 
        ('name', 'I-Drug'), 
        ('disease', 'B-Disease'), 
        ('name', 'I-Disease'), 
        ('symptom', 'B-Symptom'), 
        ('name', 'I-Symptom'), 
        ('finding', 'B-Finding'), 
        ('name', 'I-Finding'),
        ('.', 'O')]
    """
    # tokenzie the text according to this example: Stabilized	['Stabilized','approach','or','not','?','That','´','s','insane','and','good','.']
    tokened_text = 
    iob = []
    entity = "O"
    for token in tokined_text:
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


def read_data():
    """Reads the .ann and .txt files and processes the data into iob format."""

    file_names = os.listdir(OG_DATA_DIR)
    file_names = [file[:-4] for file in file_names]
    
    for file in file_names:

        file = 'ARTHROTEC.21'
        with open(OG_DATA_DIR + file + '.ann', 'r') as f, open(TXT_DATA_DIR + file + '.txt', 'r') as f2:
            ann_data = f.readlines()
            txt_data = f2.readlines()

            labels, positions = extract_data(ann_data)

            ann_txt = annotate_text(labels, positions, txt_data)
            
            iob = annotated_text_to_iob(ann_txt)

            # save_data(iob, file)

if __name__ == "__main__":
    read_data()
