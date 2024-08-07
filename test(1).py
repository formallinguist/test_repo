# -*- coding: utf-8 -*-
"""test.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18mTvvsT3XQJ3h1d3Gb1QUAzO-ME1IYSw
"""

import pandas as pd
df1 = pd.read_excel("/content/Mizo_Tacos_Train.xlsx")
df1.info()
df1.head()
df2 = df1
df2.head()
df =  pd.concat([df1, df2])
df.head()
df.info()
#converting the labels to numbers
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
df['labels'] = le.fit_transform(df.Sentiment.values)
df.head()
from sklearn.utils import shuffle
df = shuffle(df)
positive_labels = (df['labels'] == 1).sum()
negative_labels = (df['labels'] == 0).sum()
print(f"Number of positive labels: {positive_labels}")
print(f"Number of negative labels: {negative_labels}")
from sklearn.model_selection import train_test_split
train_texts, val_texts, train_labels_str, val_labels_str = train_test_split(list(df['Text']), list(df['Sentiment']), test_size=.2)
!pip install sentencepiece
!pip install transformers
!pip install transformers accelerate
!pip install torch==1.11.00.676617
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
import torch

tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-base')
model = XLMRobertaForSequenceClassification.from_pretrained('xlm-roberta-base',num_labels=2)
#print(model)

train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)

import torch

class spanish_Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_labels = le.fit_transform(train_labels_str)
val_labels = le.transform(val_labels_str)

train_dataset = spanish_Dataset(train_encodings, train_labels)
val_dataset = spanish_Dataset(val_encodings, val_labels)

from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='micro')
    acc = accuracy_score(labels, preds)
    return {'Accuracy': acc,
            'F1': f1,
            'Precision': precision,
            'Recall': recall
           }


from transformers import EarlyStoppingCallback, IntervalStrategy,Trainer, TrainingArguments
!pip install --upgrade accelerate
!pip install accelerate -U
!pip install transformers[torch]
!pip install accelerate>=0.21.0
!pip install --upgrade accelerate
import torch
torch.cuda.empty_cache()

import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"

from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=5,              # total number of training epochs 3,6,7,8
    per_device_train_batch_size=15,  # batch size per device during training
    per_device_eval_batch_size=15,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
    do_eval=True,
    evaluation_strategy="steps",
    load_best_model_at_end=True,
    eval_steps=10
)

trainer = Trainer(
    model=model,                         # the instantiated 🤗 Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset= val_dataset,
    compute_metrics=compute_metrics, # evaluation dataset
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
)

trainer.train()

