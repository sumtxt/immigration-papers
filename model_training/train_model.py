import pandas as pd
from datasets import Dataset
from setfit import SetFitModel, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def compute_metrics(y_pred, y_test):
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    return { 'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}

train_df = pd.read_csv("./model_training/usedata/train.csv")
test_df = pd.read_csv("./model_training/usedata/test.csv")

# Split in train_df and eval_df
eval_df = train_df[train_df["batch"] >= 4]
eval_df = eval_df.drop(columns=["batch"])

train_df = train_df[train_df["batch"] <= 3]
train_df = train_df.drop(columns=["batch"])

# Convert 
train_dataset = train_df.reset_index(drop=True)
train_dataset = Dataset.from_pandas(train_dataset)

test_dataset = test_df.reset_index(drop=True)
test_dataset = Dataset.from_pandas(test_dataset)

eval_dataset = eval_df.reset_index(drop=True)
eval_dataset = Dataset.from_pandas(eval_dataset)

# Infer unique labels 
labels = sorted(train_df["label"].unique())

model = SetFitModel.from_pretrained(
    "sentence-transformers/paraphrase-MiniLM-L3-v2",
    labels=labels,
)

args = TrainingArguments(
    batch_size=16,
    num_epochs=4, 
    eval_strategy="epoch",
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    metric=compute_metrics
)

# Train and evaluate
trainer.train()
metrics = trainer.evaluate(test_dataset)
print(metrics)

# Push model to the Hub
# model.push_to_hub("mmarbach/paraphrase-MiniLM-L3-v2_immig")