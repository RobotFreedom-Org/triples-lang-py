#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org   
License: MIT License  
"""  
from .utils.utils import dispatcher    

class  RoutinesTriples(object):
 
    def __init__(self:object):
        """
        Tools for creating functions ans objects
        """   
        pass 
    

    def routine(self:object, in_subjects :str = "", in_objects: str =""):
        """
        creates and manages a user routine
        
        """ 
        if in_subjects == "create":
            if in_objects == "end": 
               ## todo copy all block to function block
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
      
        elif in_subjects == "execute": 
            """
            runs a specified user routine 
            """
            cmds = self.blocks[in_objects]["code"] 
            res = []
            for cmd in cmds:   
               if cmd[0] == "run_block":
                    res  = self.routine("execute", cmd[1])
               else:
                    res = cmd[0](  cmd[1][0], cmd[1][1], cmd[1][2] ) 
    
            return res

        elif in_subjects == "load": 
            """
            runs a specified user routine 
            """
            self.memory["routine"] = self.blocks[in_objects]  
            return res

