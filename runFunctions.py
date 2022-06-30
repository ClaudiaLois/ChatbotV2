# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:16:42 2022

@author: ClaudiaLoisR
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:56:45 2022

@author: ClaudiaLoisR
"""

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
from Contexts import Info
#sub=SubcatsEN()
class RunCodes:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def __init__(self,id):
        print('new runcodes')
        self.id=id
        self.present_context='greet'
        self.missed={}
        #self.obj=DataManagement()
        self.data={}
        self.missed={}
        self.data['conv']=[]
        self.resetVariables()
        self.runNext()
        self.action=''
        self.context=0
        self.fields=[]    
        
        self.cont=1
        self.to_print={'Welcome':['Hi there! How can I help you?'],
          'Start':['Hey! Hi, What can I do for you'],
          'Sorry':['Could you please rephrase the last sentence so I can understand you better? '],
          'End':['Thanks for chatting with me!']}
        
    def resetVariables(self):
        # self.present_context='greet'     
        self.missed={}
        self.details={}
        self.data={}
        self.data['conv']=[]   
        self.i=0
        self.j=0
        self.y=0
        
        
    def runNext(self):
        self.tag_encodingEN={}
        
        with open('trainWithFunctions.json', encoding="utf8") as json_file:
            self.dataEN = json.load(json_file)
            
            
        for intent in range(len(self.dataEN['intents'])):
          self.tag_encodingEN[self.dataEN['intents'][intent]['tag']]=intent 
            
        with open('tokenizerV1.pickle', 'rb') as handle:
            self.ENtokenizer = pickle.load(handle)
            
            
    def lemmatizer(self,text):
      text = text.lower()
      sw_nltk = stopwords.words('english')
      # sw_nltk.extend(['nearby', 'near', 'want','need','work','working','needed','needing','me'])
      sw_nltk.remove('when')
      sw_nltk.remove('where')
      sw_nltk.remove('no')
      words = [word for word in text.split() if word.lower() not in sw_nltk]
      corrected=[]
      if (text.isdigit()==False):
          for word in words:
                temp = [(jaccard_distance(set(ngrams(word, 2)),
                                          set(ngrams(w, 2))),w)
                        for w in correct_words if w[0]==word[0]]
                corrected.append(sorted(temp, key = lambda val:val[0])[0][1])
          text = " ".join(corrected)
      else:
          text = " ".join(words)
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
        print('acion:',self.action)
        print('cont:',self.cont)
        print('context:',self.present_context)
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
            print('text:',text)
            if (self.action==''):
                print('inside default function')
                
                self.model=tf.keras.models.load_model('ModelV1.h5')
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
                        print('enters else')
                        self.tag, self.output_context, responses, self.action = self.best_result(prob_dict,self.dataEN)
                        output=random.choice(responses)
                        self.data['conv'].append(output)
                        self.data['context']=self.action
                        print(self.tag, self.output_context, responses, self.action)
                        #self.obj.update(self.id_,self.data)
                        print(self.data['conv'])
                        if(self.action==''):
                            yield(output,self.output_context)
                        self.context=1
                        #self.data['context']=self.action
                        #yield(output,[])
                        
            # if(self.context==0 and text in ['yes','no','yeah','nope','nah'] and self.action!=''):
            #     print('inside loop meant for confirmation')
            #     if ('yes' in text or 'yeah' in text):
            #           #response, output_context,details = getattr(Services, action)()
            #           self.data['context']=self.action
            #           self.context=1
            #           #self.Questions'],self.detailsList']=getattr(SubcatVariables, action)()
            #           # print(self.action)
    
            #     else:
            #         output=random.choice(self.to_print['Sorry'])
            #         #yield(data,missed,'MissesConv')
            #         self.data['conv'].append(output)
            #         # print(self.data['conv'])
            #         # self.obj.update(self.id_,self.data)
            #         no_match=self.data['conv'][-4]
            #         self.missed[self.tag]=no_match
            #         self.missed['time']=datetime.today()
            #         #self.obj.storeMissed(self.missed)
            #         print(output)
            #         self.missed={}
            #         self.action=''
            #         self.present_context== 'greet'
    
            #         yield(output,[])
                    
            if(self.context==1 and self.cont==1):
               print('inside loop meant for function execution')
               print('context is 1')
               self.id_= 121
               #print('inside executing functionn')
               # yield(self.action)
               #self.conv=1
               for self.j,fields,self.cont,options in getattr(Info, self.action.replace(" ", ""))(self.id_,self.data,self.details,self.fields):
                        
                        # print('first loop'+str(self.i))
                        # print(self.details)
                        if(self.i<=len(fields)):
                            self.details[fields[self.i]]=sentence
                            if(self.y==self.i):
                                # print(str(self.j))
                                self.i=self.i+1
                                self.y=0
                                self.data['conv'].append(self.j)
                                #self.obj.update(self.id_,self.data)
                                #self.context=0
                                if(self.i-1==0):
                                    print('first iteration')
                                    yield(output,options)
                                yield(self.j,options)
                            elif(self.y<self.i):
                                self.y=self.y+1
                                # print('lesser nums')
                                continue
               
            if(self.cont==0 and text in ['yes','no','No']):
                 print('inside function meant for choice after function execution')
                 self.context=0
                 self.action=''
                 self.resetVariables()
                 # print('action inside:',self.action)
                 if('yes' in text):
                     self.resetVariables()
                     self.cont=1
                     yield('What else can I help you with?',[])
                 if('no' in text):
                     print('no other help')
                     #self.resetVariables()
                     #self.present_context='bye'
                     self.action==''
                     self.cont=1
                     
                     yield('Glad I could help!',[])
                     
            # if(self.present_context== 'greet' and self.cont==0):
            #      self.action==''
            #      yield('Glad I could help!',[])
            
            
            # self.present_context=''