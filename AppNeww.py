# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:49:58 2022

@author: ClaudiaLoisR
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 11:20:29 2022

@author: ClaudiaLoisR
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 11:34:17 2021

@author: ClaudiaLoisR
"""
#from RunCode import RunCodes
#from Runn import RunCodes
from runFunctions import RunCodes
from requests import get
from bs4 import BeautifulSoup
import os
from flask import *
from flask import Flask, render_template, request, jsonify,session,redirect


app = Flask(__name__)


app.secret_key = "hello" 
session_list=[]
session_objs={}


sessionID=''
  
            
@app.route("/session=<string:sessID>/text=<string:message>", methods=['GET','POST'])
def ask(sessID,message):
        # print('session id: ' ,sessID)
        if(sessID=='0'):
            sessID=os.urandom(10)
            session['response']= str(sessID)
            chatter=RunCodes(session['response'])
           
            session_list.append(session['response'])
      
        session['response']= str(sessID)
        while True:
    
            if message == ("bye"):
    
                bot_response='Thanks for talking to me! Good bye!'
    
                return jsonify({'id':session['response'],'reply':bot_response,'options':[],'status':'OK'})
    
                break
            else:
            
                    if(session['response'] not in session_objs.keys()): 
                            print('Creating new object for session ',session['response'])
                            session_list.remove(session['response'])
                            session_objs[session['response']]=chatter
                  
                    for i,options in session_objs[session['response']].display(message):
                        
                        
                        return  jsonify({'id':session['response'],'reply':i,'options':options,'status':'OK'})


                    

if __name__ == "__main__":
    app.run(threaded=False)