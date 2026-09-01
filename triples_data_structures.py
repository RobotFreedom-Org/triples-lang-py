#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
"""  
 
from .utils.utils import dispatcher    
 
    
class  DataStructuresTriples(object):
 
    def __init__(self: object):
        """
        Functions for networked devices
        """   
        pass 
     
    
    @dispatcher      
    def structure(self : object,in_subjects :str = "", in_objects: str =""):
        """
        create a json like structure
        """   
        pass        
    
    @dispatcher
    def list(self: object, in_subject:str= "", in_objects: str ="" )-> str: 
       """ Creates a list """ 
        
       self.memory["variables_status"][in_subject]["postion"] = 0 
       self.memory["variables"][in_subject] = []
       return ""
     