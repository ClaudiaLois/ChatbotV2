import numpy as np
import json
import re
import random
import pandas as pd
import pymongo
from datetime import datetime
import tensorflow as tf
from tensorflow import keras
from keras.layers import Embedding, Bidirectional, Dense
from keras import Sequential
from tensorflow.keras.utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pdb 
import json
import pickle as pickle
from langdetect import DetectorFactory,detect,detect_langs

#print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))


 # Opening JSON file
with open('trainWithFunctions.json', encoding="utf8") as json_file:
    dataEN = json.load(json_file)


train = []
for intent in dataEN['intents']:
  tag = intent['tag'] 
  for training_phrase in intent['training_phrases']:
    row = (training_phrase.lower(), tag)
    train.append(row)

train = pd.DataFrame(train, columns=['text', 'tag'])
#train['tag'].unique()

tag_encodingEN={}
for intent in range(len(dataEN['intents'])):
  tag_encodingEN[dataEN['intents'][intent]['tag']]=intent


train['class'] = train['tag'].apply(lambda x: tag_encodingEN[x])

# Tokenization
ENtokenizer = Tokenizer(oov_token='<OOV>', filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n।')
ENtokenizer.fit_on_texts(train['text'])
# Sequencing
train_seq = ENtokenizer.texts_to_sequences(train['text'])
# Padding
train_seq = pad_sequences(train_seq, maxlen=50, truncating='post')
train_labels = train['class'].values
y_train = to_categorical(train_labels)
train_seq.shape, y_train.shape
vocab_size = len(ENtokenizer.word_index)+1

def create_model(data,vocab):
  model = tf.keras.Sequential([
          tf.keras.layers.Embedding(input_dim=vocab, output_dim=64, input_length=50),
          tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
          tf.keras.layers.Dense(64, activation='relu'),
          tf.keras.layers.Dense(16, activation='relu'),
          tf.keras.layers.Dense(len(data['intents']), activation='softmax')
  ]) 
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model

Model=create_model(dataEN,vocab=vocab_size)
Model.fit(x=train_seq, y=y_train, epochs=60, verbose=3)
Model.save('ModelV1.h5')


# saving model
    
with open('tokenizerV1.pickle', 'wb') as handle:
    pickle.dump(ENtokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)






