#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org   
License: MIT License  
"""  
from .utils.utils import dispatcher    

class  FunctionsTriples(object):
 
    def __init__(self:object):
        """
        Tools for creating functions ans objects
        """   
        pass 
    

    def create(self:object, in_subjects :str = "", in_objects: str =""):
        """
        creates a user function
        
        """ 
        if in_subjects == "function":
            if in_objects == "end": 
               self.active_blocks.pop()
              # res = self.blocks[self.s_funct ]
               self.s_funct = None  

            else:
                self.s_funct = in_objects
                self.blocks[in_objects] = {} 
                self.blocks[in_objects]["parent"] = None
                self.blocks[in_objects]["parent_type"] = None
                self.blocks[in_objects]["code"] = [] 
                self.active_blocks.append([self.s_funct , "function"])
      
        return ""
    
    @dispatcher
    def execute(self:object, in_subjects :str = "", in_objects: str =""):
        """
        runs a specified user function 
        """
        cmds = self.blocks[in_subjects]["code"] 
        res = []
        for cmd in cmds:   
           if cmd[0] == "run_block":
                res  = self.execute( cmd[1])
           else:
                res = cmd[0](  cmd[1][0], cmd[1][1], cmd[1][2] ) 

        return res

