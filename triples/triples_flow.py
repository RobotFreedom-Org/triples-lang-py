#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
"""   


class  FlowTriples(object):
 
    def __init__(self:object):
        """
        flow control functions
        """   
        pass
      
    
    def _if(self:object, in_subjects :str = "", in_objects: str =""):
         """internal function to detemrine is block of code should run """
         val1,  val2 = in_objects.split(" ") 
         condit = in_subjects(self ,  val1,  val2 ) 
         return condit

    def flow(self:object, in_subjects :str = "", in_objects: str ="start"):
        """ 
        defines a flow 
        """ 
        if in_subjects == "if":
             
            if in_objects == "start":

                parent , parent_type = None, None
                if len(self.active_blocks) > 0:
                    parent , parent_type  = self.active_blocks[-1]
                self.s_if = len(self.blocks)
                self.blocks[self.s_if] = {} 
                self.blocks[self.s_if]["parent"]      = parent
                self.blocks[self.s_if]["parent_type"] = parent_type
                self.blocks[self.s_if]["code"]        = [] 
                self.active_blocks.append([self.s_if, "if"])

            elif in_objects == "end": 
                return self._end_if(in_subjects, in_objects)

        elif in_subjects == "while":
            if in_objects == "start":
                parent , parent_type = None, None
                if len(self.active_blocks) > 0:
                    parent , parent_type  = self.active_blocks[-1]
                self.s_if = len(self.blocks)
                self.blocks[self.s_if] = {} 
                self.blocks[self.s_if]["parent"]      = parent
                self.blocks[self.s_if]["parent_type"] = parent_type
                self.blocks[self.s_if]["code"]        = [] 
                self.active_blocks.append([self.s_if, "while"])

            elif in_objects == "end": 
                return self._end_while(in_subjects, in_objects)
            
        elif in_subjects == "process":
            if in_objects == "start":
                parent , parent_type = None, None
                if len(self.active_blocks) > 0:
                    parent , parent_type  = self.active_blocks[-1]
                self.s_if = len(self.blocks)
                self.blocks[self.s_if] = {} 
                self.blocks[self.s_if]["parent"]      = parent
                self.blocks[self.s_if]["parent_type"] = parent_type
                self.blocks[self.s_if]["code"]        = [] 
                self.active_blocks.append([self.s_if, "process"])

            elif in_objects == "end":
                  
                return self._end_process(in_subjects, in_objects)


        elif in_subjects == "break":
             
                blk_id, stype = self.active_blocks[-1]   
                self.blocks[blk_id]["code"].append( [self._break, [self,  None, None ] ])  
             

        return ""

    def _break(self:object, in_subjects :str = "", in_objects: str ="", pos_1:str=None):  
        """
        breaks a  flow
        """
        self._break = True 


    def _end_while(self:object, in_subjects :str = "", in_objects: str =""):
        """
        terminates a while block
        """
        s_if      =   self.active_blocks.pop()
        self.s_if = None  
        if len(self.active_blocks) == 0: 
            self._break = False
            while True:

                if self._break:
                    break
             
                res = [] 

                for ipos, cmd in  enumerate(self.blocks[s_if[0]]["code"]): 
                
                      if cmd[0] == "run_block":
                          
                           for _ipos, cmd in  enumerate(self.blocks[cmd[1]]["code"]): 
                               if _ipos == 0:  
                                    _res =   cmd[0](self ,   cmd[1][1], cmd[1][2])  
                                   
                                    if _res != 1: 
                                        break 
                               else:     
                                    _res =   cmd[0]( cmd[1][0], cmd[1][1], cmd[1][2])   
                                    if _res != None:
                                        res.append(_res)
                      else:
                          _res =   cmd[0]( cmd[1][0], cmd[1][1], cmd[1][2])  
                          if _res != None: 
                             res.append(_res)
 
            return res 
            
        else:
             return "" 
    
    def _end_process(self:object, in_subjects :str = "", in_objects: str =""):
        """
        terminates a pprocess block
        """
        s_if      =   self.active_blocks.pop()
        self.s_if = None  
        if len(self.active_blocks) == 0: 
            self._break = False
            cmd  = self.blocks[s_if[0]]["code"][0]
            _res =   cmd[0](self ,   cmd[1][1], cmd[1][2]) 

            res = []  
            for line in _res:

                if self._break:
                    break
             
                for ipos, cmd in  enumerate(self.blocks[s_if[0]]["code"]): 
                
                      if ipos == 0: 
                           pass  
                                       
                      elif cmd[0] == "run_block":
                          
                           for _ipos, cmd in  enumerate(self.blocks[cmd[1]]["code"]): 
                               if _ipos == 0: 
                                    _res =   cmd[0](self ,   cmd[1][1], cmd[1][2])  
                                   
                                    if _res != 1: 
                                        break 
                               else:    
                                   
                                    _res =   cmd[0]( cmd[1][0], cmd[1][1], cmd[1][2])   
                                    if _res != None:
                                        res.append(_res)
                      else:
                          _res =   cmd[0]( cmd[1][0], cmd[1][1], cmd[1][2])  
                          if _res != None: 
                             res.append(_res)
 
            return res 
            
        else:
             return "" 
        
    def _end_if(self:object, in_subjects :str = "", in_objects: str =""):
        """
        terminates a if block
        """  
        s_if      =   self.active_blocks.pop()
        self.s_if = None
         
        if len(self.active_blocks) == 0:
             res = [] 
             for ipos, cmd in  enumerate(self.blocks[s_if[0]]["code"]): 
                 if ipos == 0: 
                      _res =   cmd[0](self ,   cmd[1][1], cmd[1][2])  
                      if _res != 1: 
                          break 
                 else:    
                      _res =   cmd[0]( cmd[1][0], cmd[1][1], cmd[1][2])   
                      res.append(_res)

             if len(res) == 0:
                 return ""
             else:
                 return res 
        else:
             return "" 
