#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.ord 
License: MIT License  
""" 
import random   

from .utils.utils import dispatcher  ,remap_characters_to_numbers

 
class MathTriples(object):
 
    def __init__(self:object ):
        """
        Math functions   
        """   
        self.l = {}
     
      
    @dispatcher
    def calculate(self: object, in_subject:str= "", in_objects: str ="" )-> str:
        """Evaluate a math expression safely."""
        try:
            # Only allow safe characters
            allowed_chars = "0123456789+-*/(). "
            if not all(c in allowed_chars for c in in_subject):
                return "Error: Invalid characters in expression."
            result = eval(in_subject)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation error: {e}" 


    @dispatcher
    def decrement(self: object, in_subjects:str= "", in_objects: str ="" )-> int: 
        """decrease the value of a variable """
        v1 = float(self.memory["variables"].get(in_subjects ) )
        v1 = v1 -1
        self.memory["variables"][in_subjects] =  v1  
       # v2 = float( json.loads(self.memory["variables"].get(subjects ) ))
        return v1  
       
    @dispatcher
    def increment(self: object, in_subjects:str= "", in_objects: str ="" )-> int: 
        """Increase the value of a variable """
        v1 = float( self.memory["variables"].get(in_subjects ) )
        v1 = v1 + 1
        self.memory["variables"][in_subjects] = v1  
        return v1  
    
    @dispatcher
    def add(self: object, in_subjects:str= "", in_objects: str ="" )-> int: 
        """ add two value together """
        v1 = float(  self.memory["variables"].get(in_subjects ) )
        v2 = float(  self.memory["variables"].get(in_objects ) )
        return v1  + v2 
    
    @dispatcher
    def subtract(self: object, in_subjects:str= "", in_objects: str ="" )-> int:  
        """ subtract two value together """
        v1 = float( self.memory["variables"].get(in_subjects ) )
        v2 = float(  self.memory["variables"].get(in_objects ) )
        return v1  - v2 
    
    @dispatcher
    def divide(self: object, in_subjects:str= "", in_objects: str ="" )-> int: 
        """ divide two value together """
        v1 = float( self.memory["variables"].get(in_subjects ) )
        v2 = float(  self.memory["variables"].get(in_objects ) )
        if v2 != 0:
           return v1 / v2 
        else:
           return 0.0
        
    @dispatcher
    def multiply(self: object, in_subjects:str= "", in_objects: str ="" )-> int:  
        """ multiple two value together """
        v1 = float( self.memory["variables"].get(in_subjects) )
        v2 = float(  self.memory["variables"].get(in_objects ) )
        return v1 * v2    
    
    @dispatcher 
    def roll(self: object, in_subjects:str= "", in_objects: str ="" )-> str:
        """creates a random varible based on dice""" 
        if  in_subjects.startswith('20d'):
            response  = str(random.randint(1, 20)) 
        elif  in_subjects.startswith('12d'):
            response  = str(random.randint(1, 12)) 
        elif  in_subjects.startswith('6d'):
            response  = str(random.randint(1, 6)) 
        elif  in_subjects.startswith('10d'):
            response  = str(random.randint(1, 10)) 
        elif  in_subjects.startswith('4d'):
            response  = str(random.randint(1, 4)) 
        elif  in_subjects.startswith('100d'):
            response  = str(random.randint(1, 100)) 
        elif  in_subjects.startswith('3d'):
            response  = str(random.randint(1, 3)) 
        elif  in_subjects.startswith('2d'):
            response  = str(random.randint(1, 2)) 
        elif  in_subjects.startswith('flip'):
            response  = str(random.randint(1, 2)) 
        elif  in_subjects.startswith('8d'):
            response  = str(random.randint(1, 8))   
        return response 
 