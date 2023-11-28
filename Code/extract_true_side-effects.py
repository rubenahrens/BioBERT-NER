import re
import os
import sys

from collections import defaultdict


def extract_single_file(filename, regex):

    side_effects = []

    with open(filename, 'r') as f:
        
        lines = f.readlines()

        for line in lines:
            matches = regex.findall(line)
            for match in matches:
                side_effects.append(match.strip())
        
        return side_effects


def extract_all_files(filenames):
    
    regex = re.compile(r'\d+\s*\|([\s*\w*\s*]*)')

    side_effects = []

    for filename in filenames:
        side_effects.extend(extract_single_file(filename, regex))

    side_effects_counts = defaultdict(int)
    for k in side_effects:
        side_effects_counts[k] += 1
    
    return sorted(side_effects_counts.items(), key=lambda x: x[1], reverse=True)


def get_files_disease(name):

    files = os.listdir('cadec/sct/')
    files = [f for f in files if f.startswith(name)]
    files = ['cadec/sct/' + f for f in files]

    return files


if __name__ == '__main__':

    disease = sys.argv[1]
    files = get_files_disease(disease)
    side_effects = extract_all_files(files)

    print(side_effects)