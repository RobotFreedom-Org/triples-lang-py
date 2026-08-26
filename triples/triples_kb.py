
#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
"""      
import webbrowser
from .utils.utils import dispatcher  ,replace_sep
 
class  KBTriples(object):
 
    def __init__(self:object, remote=False):
        """
        Triples Knowledge base
        """   
        pass
    

    @dispatcher
    def access(self: object, in_subjects :str = "", in_objects: str ="" )-> str:
        """
        does lookups on internal KB
        """   
 
        if in_subjects in  self.graphs:   
            if in_objects.find("dost") > -1:
                obj, verb = in_objects.split("dost", 1)
                edges = self.graphs[in_subjects].related( obj, verb, None, True )  
            else:  
                edges = self.graphs[in_subjects].related( in_objects, "current", None, True )  

            if len(edges) == 0: 
                return ""
            return  edges[0][0]["o"]  
        
        return "" 

    @dispatcher
    def define(self: object, in_subjects :str = "", in_objects: str ="" )-> str:
        """
        does lookups on internal KB
        """
        resp = "na"
        outf = None  
        scr  = -1
        if in_subjects == "word":
            in_subjects = "definitions"  

        if in_subjects in  self.graphs:  
                  
                in_objects = replace_sep(in_objects)
             
                if in_objects.find("->") > -1:
                    in_objects , outf = in_objects.split("->",1)
                    in_objects = in_objects.strip()
                    outf  = outf.strip()   
                #if lemmatise:
                #     query = [self.memory[memory_type].search_tfidf.lemmatise(w) for w in query]  
                
                resp = self.graphs[in_subjects].search_tfidf.similarities([in_objects])    
                if len(resp[0][0]) > len(resp[0][1]): 
                     resp, scr  = resp[0][0]   ,resp[0][2]   
                else:
                     resp, scr  =  resp[0][1]  ,resp[0][2]   
        else:
            resp = "na"

        if outf is not None:  

            if resp != "":
                self.set(outf, [resp , scr])   
            else: 
                self.set(outf, "na" )  
            return ""      
        else:  
            return [resp ,scr]
    
    
    @dispatcher 
    def current(self: object, in_subjects :str = "", in_objects: str ="" )-> str:
         """ 
         returns or opens a research tool
         """  
         res = ""
         if in_subjects == "time":  
             res = self.time(in_subjects, in_objects) 
         elif in_subjects == "weather":  
             webbrowser.open("https://weather.com") 
         elif in_subjects == "events":  
             webbrowser.open("https://sf.funcheap.com") 
         elif in_subjects == "calendar":  
             webbrowser.open("https://weather.com") 
         elif in_subjects == "news":  
             webbrowser.open("https://www.pbs.org/newshour/latest") 
         return res 
      
    