#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
"""  

from .utils.utils import dispatcher   
 
    
class  LogicTriples(object):
 
    def __init__(self:object):
        """
        Logic functions
        """   
        pass
      
    @dispatcher
    def more(self: object, in_subjects :str = "", in_objects: str ="" )-> int:
        """returns 1/0 if first input  is more than second"""
        v1 = float(self.memory["variables"].get(in_subjects ) )
        v2 = float( self.memory["variables"].get(in_objects ) )
       
        if v1 > v2:
            return 1
        else:
            return 0
    
    @dispatcher        
    def less(self: object, in_subjects :str = "", in_objects: str ="" )-> int:
        """returns 1/0 if first input  is less than second"""
 
        v1 = float( self.memory["variables"].get(in_subjects ) )
        v2 = float( self.memory["variables"].get(in_objects ) )


        if v1 < v2:
            return 1
        else:
            return 0 
              
      
    @dispatcher        
    def different(self: object, in_subjects :str = "", in_objects: str ="" )-> int: 
        """returns 1/0 if two inputs are different"""
        v1 = self.memory["variables"].get(in_subjects )  
        v2 = self.memory["variables"].get(in_objects )   
        if v1 != v2:
            return 1
        else:
            return 0  
    @dispatcher        
    def equal(self: object, in_subjects :str = "", in_objects: str ="" )-> int:
        """returns 1/0 if two inputs are equal"""
        v1 = self.memory["variables"].get(in_subjects )  
        v2 = self.memory["variables"].get(in_objects )   
        if v1 == v2:
            return 1
        else:
            return 0  

