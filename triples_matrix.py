#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.ord 
License: MIT License  
""" 
import random   

from .utils.utils import dispatcher  ,remap_characters_to_numbers

 
class MatrixTriples(object):
 
    def __init__(self:object ):
        """
        Matric functions   
        """   
        pass
  
    @dispatcher      
    def next(self : object,in_subjects :str = "", in_objects: str =""):
         """
         return next value from a value from stored list variables
         """   
         i = self.memory["variables_status"][in_subjects]["postion"]
         i = i +1
         fin = self.memory["variables"][in_subjects][i] 
         self.memory["variables_status"][in_subjects]["postion"] = i
         return fin  
    
    @dispatcher
    def pop(self: object, in_subjects :str = "", in_objects: str ="")-> list: 
       """sums all values in a list """ 
       fin = self.memory["variables"][in_objects] 
       res = fin.pop()
       self.memory["variables"][in_objects]  = fin
       return res 
    
    @dispatcher
    def remove(self: object, in_subjects :str = "", in_objects: str ="")-> list: 
       """appends value to a list """ 
       res =  self.memory["variables"][in_subjects][in_objects]
       del self.memory["variables"][in_subjects][in_objects]
       self.memory["variables"][in_subjects][in_objects] = res

    
    @dispatcher
    def append(self: object, in_subjects :str = "", in_objects: str ="")-> list: 
       """appends value to a list """ 
       fin = self.memory["variables"][in_objects] 
       fin.append(in_objects)
       self.memory["variables"][in_objects]  = fin

    @dispatcher
    def matrix(self: object, in_subjects :str = "", in_objects: str ="")-> list: 
       """Matrix operations """ 
       fin = self.memory["variables"][in_objects] 
       if in_subjects == "sum": 
           return sum(fin   )
       elif in_subjects == "min": 
           return min(fin  ) 
       elif in_subjects == "max": 
           return max(fin   )
       elif in_subjects == "count": 
           return len(fin )
    
    @dispatcher
    def element(self: object, in_subjects :str = "", in_objects: str ="")-> list: 
           """lRetrieves value from a list """ 
         
           fin = self.memory["variables"][in_subjects] 
           out_obj = None
           if in_objects.find("->") > -1:
               in_objects , out_obj = in_objects.split("->",1)
               out_obj = out_obj.strip()
               in_objects = in_objects.strip()
           if type(fin) == list:
                in_objects = int(in_objects)

           if out_obj is not None:
             
               self.memory["variables"][out_obj]  = fin[in_objects]  
               return ""
           else:
               return fin[in_objects] 
    
    @dispatcher
    def sort(self: object, in_subjects :str = "", in_objects: str ="")-> list: 
       """list all variables """ 
       fin = self.memory["variables"][in_subjects] 
       fin = sorted(fin)
       return fin