#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
""" 
 
import shlex 
import traceback 
import time  
   

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file")   

#Whither – literally means to where,
#whence. = from where
separators = {}
separators["whither"] = "->"
separators["whence"] = "<-" 
r_sep = {}
r_sep["->"] = "whither"
r_sep["<-"] = "whence"


def replace_sep(cmd):
    """
    replaces spoken separator
    """
    for key, val  in separators.items():
        cmd = cmd.replace(" " + key + " ", val)
        cmd = cmd.replace(key, val) 
    return cmd
 
num_mapping = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'tweleve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
    'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
    'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 80, 'hundred': 100
}

char_mapping = {
    'space': ' ' ,
}
  

def remap_characters_to_numbers(text):
    """
    replaces keywords with standard terms
    """
    for key, value in num_mapping.items():
        text = text.replace(key, value)
    return text 
 
def dispatcher(f):
    """
    Reroutes commands within accumulated blocks (like if and while)
    """
    def wrapper(*args, **kw):
        try: 

            if len(args[0].active_blocks) > 0: 
                #t_out.write(str(args) + "\n")
                if args[-1] in ["close", "end"] or args[-2] in ["close", "end"] :  
                   return f(*args, **kw)  
                     
                blk_id, stype = args[0].active_blocks[-1]  
 

                if args[0].blocks[blk_id]["parent"] is not None:
                     args[0].blocks[args[0].blocks[blk_id]["parent"]]["code"].append( ["run_block", blk_id ]) 
                if len(args) ==2:
                    args = [args[0], args[1], ""]
                return args[0].blocks[blk_id]["code"].append( [f, args ] ) 
                      
            return f(*args, **kw) 
            
        except Exception as e:  
            print(args)
            print(kw)
            print(traceback.format_exc()) 
            print("END ERROR ")   

    return wrapper  

 

def split_ignoring_quotes(text:str, parts:int=-1) -> list:
    """
    Splits a string by spaces but preserves quoted substrings.
    Supports both single and double quotes.
    """
    res = []
    def add_quote(text):

        text = text.strip() 

        if text.find(" ") > 0:
             if text.find("'")  == -1 and text.startswith('"') is False and  text.endswith('"') is False: 
                 text =  '"' +  text + '"'   
        
        return text
    try: 
        text = text.replace("'", '"')
        res = shlex.split(text)
        res = [add_quote(part) for part in res]
       # res = [part for part in res]
    except ValueError as e:
        res = [text]
 
    if parts > 0:
       if len(res) > parts:  
           return [res[0], " ".join(res[1:]) ]
       else:
           return res + ['']   
    return res


def worker_s(name):
    """Function to be executed in a separate thread."""
    print(f"[{time.strftime('%H:%M:%S')}] Thread {name} started.")
    # Simulate some work
    for i in range(3):
        print(f"[{time.strftime('%H:%M:%S')}] Thread {name} working... ({i+1}/3)")
        time.sleep(1)
    print(f"[{time.strftime('%H:%M:%S')}] Thread {name} finished.")

def list_specific_processes(prefixes):
   """List processes starting with specific prefixes."""
   matching_processes = [] 
       
   return matching_processes
