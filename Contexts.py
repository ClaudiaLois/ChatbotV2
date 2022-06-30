# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:23:51 2022

@author: ClaudiaLoisR
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 13:12:47 2021

@author: ClaudiaLoisR
"""
from DataManagement import DataManagement
from datetime import datetime

class Info:

      
  def printDict(id_,data,details):
    #details.pop('confirmation')
    if 'confirmation' in details.keys():
        details.pop('confirmation')
    if '' in details.keys():
        details.pop('')
    data['time']=datetime.today()
    data['details']=details
    print(data)
    # print('printing details',details)
    # print(globals()['data'])
    # obj=DataManagement()
    # obj.store(data,'Complete') 
    # obj.delete(id_)
    yield ('<br>Is there anything else you\'d like to ask me about?')
    
  def openingHours(id_,data,details,fields):
    fields=['confirmation','Branch',''] 
    print(data)
    yield('Which branch do you want to visit? '),fields,1
    yield('<p>Hold on while we get our executives to get you this information!'+''.join(Info.printDict(id_,data,details))),fields,0,['Go back to the main menu']
  def branchLocator(id_,data,details,fields):
    fields=['confirmation','location',''] 
    print(data)
    yield('Where do you live? '),fields,1
    yield('<p>Hold on while we get our executives to get you this information!'+''.join(Info.printDict(id_,data,details))),fields,0,['Go back to the main menu']

  def loanInformation(id_,data,details,fields):
    fields=['confirmation','Name','Number',''] 
    print(data)
    yield('What is your name? '),fields,1
    yield('Please enter your phone number: '),fields,1
    yield('<p>Hold on while we get our executives to get you this information!'+''.join(Info.printDict(id_,data,details))),fields,0,['Go back to the main menu']

    
  def goldLoan(id_,data,details,fields):
        fields=['','Name','Number','']
        yield(''),fields,1,['Avail a Gold Loan']
        yield('What is your name? '),fields,1,[]
        yield('Please enter your phone number? '),fields,1,[]
        yield('<p>I have registered your requirement. I\'ll see what I can do!'+''.join(Info.printDict(id_,data,details))),fields,0,['Go back to the main menu']

  def personalLoan(id_,data,details,fields):
        fields=['','Name','Number','']
        yield(''),fields,1,['Avail Personal Loan']
        yield('What is your name? '),fields,1,[]
        yield('Please enter your phone number? '),fields,1,[]

        yield('<p>I have registered your requirement. I\'ll see what I can do!'+''.join(Info.printDict(id_,data,details))),fields,0,['Go back to the main menu']

  def homeLoan(id_,data,details,fields):
        fields=['','Name','Number','']
        yield(''),fields,1,['How can I avail Home Loan?']
        yield('What is your name? '),fields,1,[]
        yield('Please enter your phone number? '),fields,1,[]

        yield('<p>I have registered your requirement. I\'ll see what I can do!'+''.join(Info.printDict(id_,data,details))),fields,0,['Go back to the main menu']

  def Transact(id_,data,details,fields):
        fields=['full/partial','Name','Number','']
        yield(''),fields,1,['How to get Gold Loan Topup',
                         'Gold Loan Part Payment',
                         'Pay Gold Loan Interest']
        yield('What do you want to do? '),fields,1,['full','partial']
        yield('What is your name? '),fields,1,[]
        yield('Please enter your phone number? '),fields,1,[]

        yield('<p>I have registered your requirement. I\'ll see what I can do!'+''.join(Info.printDict(id_,data,details))),fields,0,['Go back to the main menu']

  def loanAtHome(id_,data,details,fields):
        fields=['','Name','Number','']
        yield(''),fields,1,['How can I avail Loan@Home?']
        yield('What is your name? '),fields,1,[]
        yield('Please enter your phone number? '),fields,1,[]
        yield('<p>I have registered your requirement. I\'ll see what I can do!'+''.join(Info.printDict(id_,data,details))),fields,0,['Go back to the main menu']

  def goldCoins(id_,data,details,fields):
        fields=['','Name','Number','']
        yield(''),fields,1,['How to apply for gold coins?',
                            'Visit website']
        yield('What is your name? '),fields,1,[]
        yield('Please enter your phone number? '),fields,1,[]
        yield('<p>I have registered your requirement. I\'ll see what I can do!'+''.join(Info.printDict(id_,data,details))),fields,0,['Go back to the main menu']

  def jobOpenings(id_,data,details,fields):
        ffields=['','Name','Number','']
        yield(''),fields,1,['Are you looking for a job?']
        yield('What is your name? '),fields,1,[]
        yield('Please enter your phone number? '),fields,1,[]
        yield('<p>I have registered your requirement. I\'ll see what I can do!'+''.join(Info.printDict(id_,data,details))),fields,0,['Go back to the main menu']

    