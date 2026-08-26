#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
""" 

from triples.core import   Triples  
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file")   
     
if __name__ == '__main__': 
     """
     
     """

     args       =  parser.parse_args()  
     in_file    = args.file  
       
     triples  = Triples()   
   
     if in_file is not None:
          
          resp  =  triples.run(in_file)

          for line in resp:
              print(line)
     else:     
        while True:
          
          cmds = input(">")
          if cmds.endswith(";"):
              cmds = cmds[:-1]
          obj, prep = "",""

          if cmds.find(" ") > -1: 
              cmd, params =  triples.split_ignoring_quotes(cmds,1) #.split(' ', 1) 
              cmd = cmd.strip()

              if params.find(" ") > -1: 
                  obj, prep =  triples.split_ignoring_quotes(params , 1) 
              else:
                  obj =  params.strip()
          else:
              cmd, obj, prep = cmds , "", ""

          resp =  getattr(triples, "%s" % cmd.lower().strip() )(obj, prep) 
          print( resp)


    