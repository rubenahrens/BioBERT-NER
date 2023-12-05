from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')


def annotated_text_to_iob(ann_text):
    """Converts the annotated text to IOB format.
        # Input text:
        # <ADR> Side effect name </ADR> <Drug> Drug name </Drug> <Disease> Disease name </Disease> 
        # <Symptom> Symptom name </Symptom> <Finding> Finding name </Finding>.
        # We turn this into:
        # [('side', 'B-ADR'), 
        # ('effect', 'I-ADR'), 
        # ('name', 'I-ADR'), 
        # ('drug', 'B-Drug'), 
        # ('name', 'I-Drug'), 
        # ('disease', 'B-Disease'), 
        # ('name', 'I-Disease'), 
        # ('symptom', 'B-Symptom'), 
        # ('name', 'I-Symptom'), 
        # ('finding', 'B-Finding'), 
        # ('name', 'I-Finding'),
        # ('.', 'O')]
    """
    tokined_text = tokenizer.tokenize(ann_text)
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


# Test case 1: Basic example
ann_text = "<ADR> Side effect name </ADR> <Drug> Drug name </Drug> <Disease> Disease name </Disease> <Symptom> Symptom name </Symptom> <Finding> Finding name </Finding>."
expected_output = [('side', 'B-ADR'), ('effect', 'I-ADR'), ('name', 'I-ADR'), ('drug', 'B-Drug'), ('name', 'I-Drug'), ('disease', 'B-Disease'), ('name', 'I-Disease'), ('symptom', 'B-Symptom'), ('name', 'I-Symptom'), ('finding', 'B-Finding'), ('name', 'I-Finding'), ('.', 'O')]
print(annotated_text_to_iob(ann_text))
assert annotated_text_to_iob(ann_text) == expected_output

# Test case 2: Empty input
ann_text = ""
expected_output = []
assert annotated_text_to_iob(ann_text) == expected_output

# Test case 3: No annotations
ann_text = "This is a sample text without any annotations."
expected_output = [('This', 'O'), ('is', 'O'), ('a', 'O'), ('sample', 'O'), ('text', 'O'), ('without', 'O'), ('any', 'O'), ('annotations', 'O'), ('.', 'O')]
assert annotated_text_to_iob(ann_text) == expected_output

# Test case 4: Multiple annotations of the same type
ann_text = "<ADR> Side effect name </ADR> <ADR> Another side effect </ADR>."
expected_output = [('side', 'B-ADR'), ('effect', 'I-ADR'), ('name', 'I-ADR'), ('another', 'B-ADR'), ('side', 'I-ADR'), ('effect', 'I-ADR'), ('.', 'O')]
assert annotated_text_to_iob(ann_text) == expected_output

# Test case 5: Nested annotations
ann_text = "<ADR> Side effect <Drug> Drug name </Drug> </ADR>."
expected_output = [('side', 'B-ADR'), ('effect', 'I-ADR'), ('drug', 'B-Drug'), ('name', 'I-Drug'), ('.', 'O')]
assert annotated_text_to_iob(ann_text) == expected_output

print("All test cases passed!")