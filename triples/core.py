#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
""" 
import glob
import json
import subprocess 
  
from  .triples_math import MathTriples 
from  .triples_string import StringTriples 
from  .triples_logic import LogicTriples 
from  .triples_flow import FlowTriples 
from  .triples_functions import FunctionsTriples 
from  .triples_temporal  import TemporalTriples 
from  .triples_media import MediaTriples 
from  .triples_file import FileTriples 
from  .triples_kb import KBTriples 
from  .triples_misc  import MiscTriples  
from  .triples_matrix import MatrixTriples
ROOT = "./triples/"  
 
from .utils.utils import dispatcher  ,replace_sep, split_ignoring_quotes
 

class CoreTriples():

        def __init__(self : object, *param):
            """
            core functions for Triples
            """   
           
            self.graphs = {}  
            self.memory = {}
            self.memory["files"] = {}
            self.memory["log"]   = {}
            self.memory["variables"]   = {} 
            self.memory["variables_status"]   = {} 
            self.memory["scratch"]   = {} 
            self.blocks        = {}
            self.active_blocks = []  


        def annotation(self: object, in_subjects :str = "", in_objects: str ="")-> list: 
            return None
        
        @dispatcher
        def memory(self: object, in_subjects :str = "", in_objects: str ="")-> list: 
           """list all variables """
           if in_subjects == "list":
               pass
           elif in_subjects == "clear":
               pass
           elif in_subjects == "save":
               pass
           elif in_subjects == "load":
               pass
           return self.memory["variables"] 

        @dispatcher
        def copy(self: object, in_subjects :str = "", in_objects: str ="")-> list: 
           """copies one variable to another position """
           self.memory["variables"][in_objects] = self.memory["variables"][in_subjects] 
           return ""

        
        @dispatcher    
        def set(self : object, in_subjects :str = "", in_objects: str =""):
            """
            sets a variable 
            """    
            if type(in_objects) == str: 
                in_objects = replace_sep(in_objects) 
    
                if in_objects.find("<-") > -1:
    
                    _t , vars = in_objects.split("<-",1)
    
                    cmd, vars    = split_ignoring_quotes(vars ,1 )  
                    obj2, prep2  = split_ignoring_quotes(vars ,1 )  
     
                    in_objects =  getattr(self, "%s" % cmd.lower().strip())(obj2, prep2) 

            self.memory["variables"][in_subjects] = in_objects
            return ""
        
        @dispatcher      
        def get(self : object, in_subjects :str = "", in_objects: str =""):
            """
            gets a variables
            """    
            if in_subjects in  self.memory["variables"]:
                return self.memory["variables"][in_subjects]
            else:
                return ""

        
        @dispatcher         
        def echo(self: object, in_subjects :str = "", in_objects: str ="")-> str:
             """
             writes variable to file or shell 
             """ 
             if   type(in_subjects) is str:
                if in_subjects.startswith('"') is False and in_subjects.startswith("'") is False and in_subjects.find(" ")  == -1: 
                 
                     try:
                         v = self.memory["variables"].get( in_subjects) 
                     except:
                         v = None

                     if v is not None and v != "": 
                        in_subjects = v
             
             if in_objects == "shell": 
                 
                 print(in_subjects)
                 return ""
             
             elif in_objects not in ["out" , ""]:  
                 result = subprocess.run("echo " + str(in_subjects) + " > " + in_objects, shell=True, stdout=subprocess.PIPE)
                 res  = result.stdout.decode('utf-8') 
                 return "created " + in_objects
             
             else:    
                 if type(in_subjects) == str:
                     in_subjects = in_subjects.replace('"' , "")
                 return in_subjects 
 
class Triples(CoreTriples, MathTriples, StringTriples, LogicTriples, FlowTriples, 
              FunctionsTriples, TemporalTriples, MediaTriples, FileTriples,
              KBTriples, MiscTriples,MatrixTriples):

    def __init__(self : object,   **kwargs ):
        """
        
        """
        CoreTriples.__init__(self)
        MathTriples.__init__(self)
        StringTriples.__init__(self)
        LogicTriples.__init__(self)
        FlowTriples.__init__(self)
        FunctionsTriples.__init__(self)
        TemporalTriples.__init__(self)
        MatrixTriples.__init__(self)
        
        ##optionals
        FileTriples.__init__(self)
        MediaTriples.__init__(self)
        KBTriples.__init__(self)
        MiscTriples.__init__(self)  

        self.docs = {}

        
        for file in glob.glob(ROOT + "docs/*.json"):
           with open(file) as f:
               s_json = ""
               for line in f:
                   s_json += line
               doc = json.loads(s_json)
               for k, v in doc.items():
                   self.docs[k] = v 
     
        self.functions      = [f for f in dir(self) if f.startswith("_") is False]   
        self.function_lkup  =   self.functions 

        try:
            from trpl_graph import TrplGraph
            from router import Router
        except:
            from .trpl_graph import TrplGraph
            from .router import Router
        
        self.TrplGraph            = TrplGraph  
        self.graphs["router"]     = TrplGraph()  
        self.graphs["scratch"]    = TrplGraph()  
 
        self.router        = Router(self.docs,
                             self.functions , 
                             ROOT,
                             self.graphs["router"] )

        if "robot" in kwargs:
            self.robot = kwargs["robot"]

        if "config" in kwargs:
            self.config = kwargs["config"]

        if "communication" in kwargs:
            self.communication = kwargs["communication"] 
    
    @dispatcher 
    def help(self : object,  in_subjects :str = "", in_objects: str =""):
        """
        """
        #if cmd == "help":
        #self.robot_text = " ".join([p for p in dir(self.functions) if p.startswith("__") is False])
           
        cmds = []
        if in_subjects == "": 
          for key, details in self.docs.items(): 
            if details["type"] == "function":
                val = details["function"]
                mess = key  
                cmds.append(mess)
        else:
            if in_subjects in self.docs: 
                val = self.docs[in_subjects]["function"]
                mess = key + " " + val["description"]   
                mess += "\n  Params " + " ".join(list(val["parameters"].keys()))    
                mess += "\n  Example " + val["example"]
                cmds.append(mess)
            else:
                cmds.append(obj =" not found")

        return sorted(cmds)

  #  @dispatcher
    def run(self: object, in_subjects :str = "", in_objects: str ="")-> str: 

        if type(in_subjects) == dict:
            part_1, part_2 , part_3  = in_subjects["v"], in_subjects["s"], in_subjects["o"]
            res = getattr(self  , "%s" % part_1.lower().strip())(part_2, part_3)
            return  res
        
        elif type(in_subjects) == list:
            res = []
            for cmd in in_subjects:
                #cmd =  json.loads(line.strip())
                _res= self.run(cmd) 
                if _res is not None and _res != "":
                    res.append(_res) 
            if len(res) == 0:
               return [""]
            else:
                return  res[-1]
        
        elif  in_subjects.endswith(".trpls") is False:
 
            parts = split_ignoring_quotes(in_subjects.replace(";","")) 

            if len(parts) == 0:
                return None
            elif len(parts) ==1:
                 part_1, part_2 , part_3  = parts[0], "", ""

            elif len(parts) ==2:
                 part_1, part_2 , part_3  = parts[0], parts[1], ""

            elif len(parts) ==3:
                 part_1, part_2 , part_3  = parts[0], parts[1], parts[2] 
            else:
                 part_3 = " ".join(parts[2:] )

                 part_1, part_2   = parts[0], parts[1]  

            res = getattr(self  , "%s" % part_1.lower().strip())(part_2, part_3)
            return  res
        
        response = []
        
        with open(in_subjects, 'r') as in_data:   
            for row in in_data: 
               row =row.strip() 
               if row.endswith(";"):
                   row = row[:-1]
               part_1, part_2 , part_3  = row,"",""
               if row.find(" ") > -1: 
                   part_1 , part_2 =  split_ignoring_quotes(row,1)

                   if part_2.find(" ") > -1:
                       part_2 , part_3 = split_ignoring_quotes(part_2, 1)   
                       if part_3 == None:
                           part_3 = "" 

               cmd = part_1.lower().strip()

               if row.find("@") > 0:   
                    self.__send_cmd("remote_cmd",  row)   
               elif cmd != "":
                    res = getattr(self, "%s" % part_1.lower().strip())(part_2, part_3) 
               else:
                    res = ""

               if res != "" and res is not None:     
                    try:
                       res =str(res)
                    except:
                       print(cmd, res)   
                    

                    response.append(res)

        return response
        