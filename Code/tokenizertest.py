from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

# Tokenize a single sentence
tokens = tokenizer.tokenize("Hello, Hugging Face!")
print(tokens)