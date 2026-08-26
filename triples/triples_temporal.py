#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: HipMonsters.com  
License: MIT License  
""" 
 
import time  
import datetime     
from .utils.utils import dispatcher    
    
class  TemporalTriples(object):
 
    def __init__(self:object):
        """
        Time and date functions
        """   
        pass
  
    @dispatcher          
    def datetime(self: object, in_subjects:str= "",in_objects: str ="" )-> str:
        """Return the current datetime """
        return  datetime.datetime.now()  
    
    @dispatcher
    def date(self: object, in_subjects:str= "",in_objects: str ="" )-> str:
        """Return current date in string format."""
 
        resp = "the date is " + datetime.datetime.now().strftime("%B %d %Y")
        return [resp] 
    
    @dispatcher
    def time(self: object, in_subjecst:str= "",in_objects: str ="" )-> str:
        """Return current time in string format."""
        resp = "the time is " + datetime.datetime.now().strftime("%H o clock and %M minutes")
        return [resp] 

    @dispatcher
    def temporal(self: object, in_subjects:str= "",in_objects: str ="" )-> str:
        """sleeps"""
        if in_subjects == "pause":
            time.sleep(1)
        return ""
     
