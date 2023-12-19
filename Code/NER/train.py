# MIT licensed
import datasets
from transformers import Trainer, TrainingArguments, AutoTokenizer, AutoModelForTokenClassification, DataCollatorForTokenClassification
from huggingface_hub import interpreter_login
import evaluate
import numpy as np
from sklearn.metrics import precision_recall_fscore_support


ENTITIES = ['O',
            'B-ADR', 'B-Disease', 'B-Drug', 'B-Symptom', 'B-Finding',
            'I-ADR', 'I-Disease', 'I-Drug', 'I-Symptom', 'I-Finding']

metric = evaluate.load("seqeval")


def compute_metrics(eval_preds):
    """Compute metrics for evaluation."""

    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)

    true_labels = [[ENTITIES[l] for l in label if l != -100] for label in labels]
    true_predictions = [
        [ENTITIES[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    all_metrics = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": all_metrics["overall_precision"],
        "recall": all_metrics["overall_recall"],
        "f1": all_metrics["overall_f1"],
        "accuracy": all_metrics["overall_accuracy"],
    }


def train(tokenized_datasets):
    """Train model on training data."""

    model_checkpoint = "bert-base-cased"
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

    id2label = {i: label for i, label in enumerate(ENTITIES)}
    label2id = {v: k for k, v in id2label.items()}

    model = AutoModelForTokenClassification.from_pretrained(
        model_checkpoint,
        id2label=id2label,
        label2id=label2id,
    )

    training_args = TrainingArguments(
        "bert-finetuned-ner",
        evaluation_strategy="epoch",
        logging_strategy="no",
        save_strategy="no",
        learning_rate=2e-5,
        num_train_epochs=3,
        weight_decay=0.01,
        push_to_hub=True,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
        compute_metrics=compute_metrics,
        tokenizer=tokenizer,
    )
    trainer.train()
    trainer.push_to_hub(commit_message="Training complete")


def main():

    # Load data
    processed_datasets = datasets.load_from_disk('cadec/processed')
    
    print(processed_datasets)

    # Train model
    train(processed_datasets)



if __name__ == '__main__':
    main()