#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
""" 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file")   
     

from .core import   Triples 

if __name__ == '__main__': 
     """
     
     """

     args       =  parser.parse_args()  
     in_file    = args.file 
     
     
     import os, sys
     os.chdir('../')
     sys.path.insert(0, os.path.abspath('./')) 
 
     import config  
     from communication.client    import Client
     from communication.nerves    import Nerves    

     from communication.network    import map_rf_ips_quick
     from devices.tools            import scan_serial_ports
     from devices.wearable_sync    import scan_for_ble
     
     settings = {}
     nerves = Nerves("User")
      

     communication_ip   = list(config.NET_CONFIG["hubs"].keys())[0]   
     communication  = None
     if communication_ip is not None:
           try:
              communication = Client( "user", communication_ip)
              communication.connect()
           except: 
              communication  = None
      
     triples  = Triples(agent="user", 
                        config=config,
                        communication=communication,
                        nerves=nerves,
                        client=True, 
                        networked=1, 
                        lt_mem = None)   

     from memory.lt_memory import LTMemory

     lt_mem        =  LTMemory("squirrel", 
                               config, 
                               triples= triples, 
                               load_all=True) 
    
     triples.kb = lt_mem.memory["definitions"]
     
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


    