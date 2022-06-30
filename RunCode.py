# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:24:10 2021

@author: ClaudiaLoisR
"""
import jsonpickle
from requests import get
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template, request, jsonify
# from ChatbotCode import Startchat 
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
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

from DataManagement import DataManagement
nltk.download('words')
from nltk.corpus import words
correct_words = words.words()
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams

#sub=yield()
class RunCodes:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def __init__(self,id):
        self.id=id
        self.present_context='greet'    
        #self.obj=DataManagement()
        self.data={}
        self.missed={}
        self.data['conv']=[]
        self.resetVariables()
        self.runNext()
        self.action=''
        self.to_print={'Welcome':['Hi there! How can I help you?'],
          'Start':['Hey! Hi, What can I do for you'],
          'Sorry':['Could you please rephrase the last sentence so I can understand you better? '],
          'End':['Thanks for chatting with me!']}
        
    def resetVariables(self):
        self.present_context='greet'     
        self.missed={}
        self.details={}
        self.data={}
        self.data['conv']=[]   

        
        
    def runNext(self):
        self.tag_encodingEN={}
        
        with open('trainNeww.json', encoding="utf8") as json_file:
            self.dataEN = json.load(json_file)
            
            
        for intent in range(len(self.dataEN['intents'])):
          self.tag_encodingEN[self.dataEN['intents'][intent]['tag']]=intent 
            
        with open('tokenizer.pickle', 'rb') as handle:
            self.ENtokenizer = pickle.load(handle)
            
            
    def lemmatizer(self,text):
      text = text.lower()
      sw_nltk = stopwords.words('english')
      # sw_nltk.extend(['nearby', 'near', 'want','need','work','working','needed','needing','me'])
      sw_nltk.remove('when')
      sw_nltk.remove('where')
      words = [word for word in text.split() if word.lower() not in sw_nltk]
      corrected=[]
      for word in words:
            temp = [(jaccard_distance(set(ngrams(word, 2)),
                                      set(ngrams(w, 2))),w)
                    for w in correct_words if w[0]==word[0]]
            corrected.append(sorted(temp, key = lambda val:val[0])[0][1])
      text = " ".join(corrected)
      #print(text)
      return text
  
    def preprocess(self,sentence):
        
        if isinstance(sentence, list):
          seq = self.ENtokenizer.texts_to_sequences(sentence.lower())
           
          
        else:
          seq = self.ENtokenizer.texts_to_sequences([sentence.lower()])
        seq = pad_sequences(seq, maxlen=50, truncating='post')
        return seq
         
    def get_class_probab_eng(self,prediction):
      probab_dict = {}
      i = 0
      for label in self.tag_encodingEN:
        prob = prediction[0][i]
        probab_dict[label] = prob
        i += 1
      return probab_dict
    def get_contexts(self,tag, data):
      for intent in data['intents']:
        if intent['tag']==tag:
          return intent['in_context'], intent['out_context'], intent['responses'], intent['action']
    
    def best_result(self,probab_dict, intents_data, error_thres = 0.4, present_context = ''):
      
      valid_tags = [[key, value, self.get_contexts(key, intents_data)] for key, value in probab_dict.items() if (value>=error_thres) and self.get_contexts(key, intents_data)[0]==present_context]
    
      if len(valid_tags)==0:
        return None
      else:
        valid_tags.sort(key=lambda x: x[1], reverse=True) 
         # sort so that 1st row has max prob
        return valid_tags[0][0], valid_tags[0][2][1], valid_tags[0][2][2], valid_tags[0][2][3]
     
            
    def display(self,message):
        # print('present context =',self.present_context)

        if self.present_context != 'bye':
            flag=False     
            cont=0
            #self.resetVariables()
            #output='start--'
            self.data['time']=datetime.today()
            #self.data['conv'].append(output)
            #self.id_=self.obj.insert(self.data)
            sentence = message.strip().lower()
            self.data['conv'].append(sentence)
            #self.obj.update(self.id_,self.data)
            text = self.lemmatizer(sentence)

            self.model=tf.keras.models.load_model('Model.h5')
            print('model loaded')
            seq = self.preprocess(text)
                # print('Tokenized phrase:',seq)
                # yield (text)
            prediction = self.model.predict(seq)
            prob_dict = self.get_class_probab_eng(prediction)
                #print('probability dictionary:',prob_dict)
            highest= max(prob_dict,key=lambda x: prob_dict[x])
            if self.best_result(prob_dict,self.dataEN) is None:
                    output=random.choice(self.to_print['Sorry'])
                    self.data['conv'].append(output)
                    #self.obj.update(self.id_,self.data)
                    no_match=self.data['conv'][-2]
                    # self.missed['Not matched']=no_match
                    # self.missed['time']=datetime.today()
                    # self.obj.storeMissed(self.missed)
                    # self.missed={}
                    yield(output,[])
                    
            else:
                    self.tag, self.output_context, responses, self.action = self.best_result(prob_dict,self.dataEN)
                    output=random.choice(responses)
                    self.data['conv'].append(output)
                    #self.obj.update(self.id_,self.data)
                    print(self.data['conv'])
                    print(self.output_context)
                    yield(output,self.output_context)
                    
            self.resetVariables()
            
            # self.present_context=''