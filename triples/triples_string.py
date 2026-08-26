#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: HipMonsters.com  
License: MIT License  
""" 
 
from .utils.utils import dispatcher  , split_ignoring_quotes, replace_sep
 
  
class  StringTriples(object):
 
    def __init__(self:object):
        """
        String functions
        """   
        pass 
    
    @dispatcher
    def split(self: object, in_subjects:str= "",in_objects: str ="" )-> int: 
        """joins two string together"""
        v1 = self.memory["variables"].get(in_subjects ) 
        return v1.split(in_objects)

    @dispatcher
    def lower(self: object, in_subjects:str= "",in_objects: str ="" )-> int: 
        """joins two string together"""
        v1 = self.memory["variables"].get(in_subjects ) 
        return v1.lower()
    
    @dispatcher
    def upper(self: object, in_subjects:str= "",in_objects: str ="" )-> int: 
        """joins two string together"""
        v1 = self.memory["variables"].get(in_subjects ) 
        return v1.upper()
    
    
    @dispatcher
    def replace(self: object, in_subjects:str= "",in_objects: str ="" )-> int: 
        """joins two string together"""
        v1 = self.memory["variables"].get(in_subjects ) 
        in_objects = replace_sep(in_objects)
        frm, to = in_objects.split("->")
        return v1.replace(frm, to)
    
    
    @dispatcher
    def join(self: object, in_subjects:str= "",in_objects: str ="" )-> int: 
        """joins two string together"""
        in_objects = split_ignoring_quotes(in_objects )
        res = [in_subjects] +  in_objects

        fin = []
        for wrd in res:
            try: 
              _wrd = self.memory["variables"].get(wrd.strip()) 
            except:
              _wrd = wrd
            if _wrd != "" and _wrd is not None:
              wrd = _wrd
            fin.append(wrd)

        return  " ".join(fin)
 