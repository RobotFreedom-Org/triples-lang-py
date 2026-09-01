#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
"""  
from .utils.utils import dispatcher   
 
class  FileTriples(object):
 
    def __init__(self:object):
        """
        File functions
        """   
        pass 

    @dispatcher
    def file(self: object, in_subjects :str = "", in_objects: str ="" )-> str:
        """Read a text file."""
        
        if in_subjects == "list":
            return self.memory["files"].keys()
        
        elif in_subjects == "close": 
            s_if , s_type =  self.active_blocks.pop() 
            if len(self.active_blocks) == 0:
              
                res = [] 
                for row in self.memory["files"][s_if]:
                      
                     for ipos, cmd in  enumerate(self.blocks[s_if]["code"]): 
                        
                          params = list(cmd[1])

                          if params[0] == "row":
                             params[0] = row.strip()

                          if params[1] == "row":
                             params[1] = row.strip()

                          if params[2] == "row":
                             params[2] = row.strip()
                              
                          _res =   cmd[0]( params[0], params[1], params[2])  
                          res.append(_res)
    
                return res 
            
            return ""
           
        elif in_subjects == "read":
            
            try:

                parent , parent_type = None, None
                if len(self.active_blocks) > 0:
                    parent , parent_type  = self.active_blocks[-1]

                self.s_if = len(self.blocks)
                self.blocks[self.s_if] = {} 
                self.blocks[self.s_if]["parent"]      = parent
                self.blocks[self.s_if]["parent_type"] = parent_type
                self.blocks[self.s_if]["code"]        = []   
                self.active_blocks.append([self.s_if, "file"])

                self.memory["files"][self.s_if] = open(in_objects, "r", encoding="utf-8")  
  
            except FileNotFoundError:
                 return "Error: File not found."
            except Exception as e:
                return f"File read error: {e}"
