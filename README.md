# Fine-Tuning BioBERT on Medical Text

A Text Mining project by Lucas de Wolf (s3672980) and Ruben Ahrens (s3677532)

## Project Overview

This project focuses on Named Entity Recognition (NER) in medical text, specifically using the CSIRO Adverse Drug Event Corpus (CADEC). We fine-tuned transformer-based models (BERT and BioBERT) to identify medical entities in patient-reported adverse drug event narratives.

## Repository Structure

- `/bert-finetuned-ner/`: Contains fine-tuned BERT models for named entity recognition
- `/cadec/`: The CSIRO Adverse Drug Event Corpus dataset
  - `/meddra/`: MedDRA annotations
  - `/original/`: Original text data
  - `/processed/`: Processed dataset
  - `/sct/`: SNOMED CT annotations
  - `/text/`: Raw text files
- `/Code/`: Project source code
  - `/NER/`: Named entity recognition implementation
    - `NER_bert.ipynb`: Implementation of BERT for NER
    - `NER_biobert.ipynb`: Implementation of BioBERT for NER
  - `/Entity Linking/`: Code for entity linking tasks
  - `datastats.py`: Script for dataset statistics
  - `test.py`: Testing script
- `/Results/`: Experimental results and output data

## Technologies Used

- Python with HuggingFace Transformers
- BERT and BioBERT models
- Jupyter Notebooks
- scikit-learn for evaluation metrics

## Getting Started

To run the notebooks:
1. Ensure all dependencies are installed
2. Run the Jupyter notebooks in the `/Code/NER/` directory

## Citation

If you use the CADEC dataset:
- Karimi et al. (2015) CADEC: A corpus of adverse drug event annotations
- Data: https://data.csiro.au/collection/csiro:10948

## Contributors

- Lucas de Wolf (s3672980)
- Ruben Ahrens (s3677532)

January 2024