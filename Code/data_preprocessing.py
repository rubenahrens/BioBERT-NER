"""
here we will make IOB files from text in the ../cadec/text files
the IOB files will be in the cadec/iob directory
the entities are in the y column of the cadec/sct files where each line is like this: x | y | z
example: TT1	271782001 | Drowsy | 9 19	bit drowsy
the first two numbers of the z column are the start and end of the character indices for the entity in the text

The IOB format is like this:
doc1token1 tag1
doc1token2 tag2
doc1token3 tag3
doc1token4 tag4
doc1token5 tag5
doc1token6 tag6

doc2token1 tag1
doc2token2 tag2
doc2token3 tag3
doc2token4 tag4
doc2token5 tag5

etc.
"""

import os
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')


def make_iob_files():
    for file in os.listdir('cadec/text'):
        with open('cadec/text/' + file, 'r') as f:
            text = f.read()
        with open('cadec/sct/' + file[:-4] + '.ann', 'r') as f:
            sct = f.read()
        sct = sct.split('\n')
        iob = ''
        i=0
        text_tokens = tokenizer.tokenize(text)
        text_token_tuples = [(token, "O") for token in text_tokens]
        print(text_token_tuples)
        for line in sct:
            if "CONCEPT_LESS" not in line and line != '':
                # TODO: don't just  pick the first entity if there are multiple
                entity = line.split('|')
                start_end = entity[-1].split('\t')[0].strip()
                # TODO: handle multiple entities in one line (e.g. 9 19; 21 30) like in file ARTHROTEC.104.ann
                # if ";" in start_end:
                #     start_end = start_end.split(';')
                #     for indices in start_end:
                #         start = int(indices.split(' ')[0].strip())
                #         end = int(indices.split(' ')[1].strip())
                #         entity = entity[1].strip()
                if ";" not in start_end:
                    start = int(start_end.split(' ')[0].strip())
                    end = int(start_end.split(' ')[1].strip())
                    entity = entity[1].strip()
                    # TODO: go from character indices to token indices
                    zero_tokens = tokenizer.tokenize(text[i:start])
                    for token in zero_tokens:
                        iob += token + ' O\n'
                    entity_tokens = tokenizer.tokenize(text[start:end])
                    iob += entity_tokens[0] + ' B-' + entity + '\n'
                    for token in entity_tokens[1:]:
                        iob += token + ' I-' + entity + '\n'
                    i = end
        zero_tokens = tokenizer.tokenize(text[i:])
        for token in zero_tokens:
            iob += token + ' O\n'
    with open('cadec/iob/' + file[:-4] + '.iob', 'w') as f:
        f.write(iob)

if __name__ == '__main__':
    make_iob_files()