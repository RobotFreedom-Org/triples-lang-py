#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
""" 
import sys


from triples.utils.utils import dispatcher  ,replace_sep, split_ignoring_quotes
from triples.core import   Triples  
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default=None)  
parser.add_argument("-l", "--library", default=None)   
parser.add_argument("-p", "--parameters", default=None)   
parser.add_argument("-r", "--routine", default=None)   
parser.add_argument("-t", "--type", default="jsonl")   
     
if __name__ == '__main__': 
     """
     cat simple_data.jsonl | python triples-lang.py -f stdin -l simple_engine.trpl -r test -p prompt,response
     python triples-lang.py -f simple_data.jsonl  -l simple_engine.trpl -r test -p prompt,response
     """

     args          = parser.parse_args()  
     in_file       = args.file  
     in_libray     = args.library  
     in_routine    = args.routine  
     in_params     = args.parameters  
     in_file_type  = args.type  
       
     triples  = Triples()   
   
     if in_file is not None:

          if in_libray is not None:

               triples.process("library"     , in_libray)
               triples.process("routine"     , in_routine)
               triples.process("map"         , in_params.split(",")) 
               triples.process("format"      , in_file_type) 

               if  in_file.startswith("stdin"): 
                 for line in sys.stdin.read():
                     resp  =  triples.process("row", line.strip())
                     print(resp)
               else: 
                 for line in open("simple_data.jsonl"):  
                     resp  =  triples.process("row", line.strip())
                     print(resp)

          else: 
              resp  =  triples.run(in_file) 
              for line in resp:
                  print(line)
     else:     
        while True:
          
            cmds = input(">")
            if cmds.endswith(";"):
                cmds = cmds[:-1]

            if cmds == "bye": 
                 sys.exit()
                 
            obj, prep = "",""
  
            if cmds.find(" ") > -1: 
                cmd, params =   split_ignoring_quotes(cmds,1)  
                cmd = cmd.strip()
  
                if params.find(" ") > -1: 
                    obj, prep =  split_ignoring_quotes(params , 1) 
                else:
                    obj =  params.strip()
            else:
                cmd, obj, prep = cmds , "", ""
  
            resp =  getattr(triples, "%s" % cmd.lower().strip() )(obj, prep) 
            print( resp)


    