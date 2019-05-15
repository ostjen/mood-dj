#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from flair.data_fetcher import NLPTaskDataFetcher
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentLSTMEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from pathlib import Path

#shuffle the dataframe
data = pd.read_csv('./data/classifier-data.csv').sample(frac = 1).drop_duplicates()

#flair input
data['label'] = '__label__' + data['label'].astype(str)

# split into train and test data (80:20 proportion)

data.iloc[0:int(len(data)*0.8)].to_csv('train.csv', sep='\t', index = False, header = False, columns=['label', 'quote'])
data.iloc[int(len(data)*0.8):int(len(data)*0.9)].to_csv('test.csv', sep='\t', index = False, header = False, columns=['label', 'quote'])
data.iloc[int(len(data)*0.9):].to_csv('dev.csv', sep='\t', index = False, header = False, columns=['label', 'quote'])

#create classifier model using LSTM word embeddings

corpus = NLPTaskDataFetcher.load_classification_corpus(Path('./'), test_file='test.csv', dev_file='dev.csv', train_file='train.csv')
word_embeddings = [WordEmbeddings('glove'), FlairEmbeddings('news-forward-fast'), FlairEmbeddings('news-backward-fast')]
document_embeddings = DocumentLSTMEmbeddings(word_embeddings, hidden_size=512, reproject_words=True, reproject_words_dimension=256)
classifier = TextClassifier(document_embeddings, label_dictionary=corpus.make_label_dictionary(), multi_label=False)
trainer = ModelTrainer(classifier, corpus)
trainer.train('./', max_epochs=20)
