#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.com  
License: MIT License  
""" 
 
import webbrowser 
try:
    from PIL import Image 
except:
    print("PIL for images not loaded")
 
from .utils.utils import dispatcher    
 
    
class  MediaTriples(object):
 
    def __init__(self:object):
        """
        Media functions
        """   
        pass
      
     

    @dispatcher
    def media(self: object, in_subject:str= "", in_objects: str ="" )-> dict: 

        if in_subject == "commense":  
            if in_objects == "video":  
                self.__send_cmd("remote_cmd",  "video:" + obj) 
                res = "taking video"
            elif in_objects == "snapshot": 
                self.__send_cmd("remote_cmd",  "snapshot:" + obj) 
                res = "taking photo"
            elif in_objects == "recording": 
                self.__send_cmd("remote_cmd",  "recording:" + obj) 
                res = "recording sound"

        elif in_subject == "open": 

            in_objects = in_objects.split(" ")
            if in_objects[0] == "browser":  
                 url  ="https://hipmonsters.com" 
                 if len(in_objects)  > 1:
                     url = in_objects[1]
                 webbrowser.open(url)

            elif in_objects[0] == "music": 
                 self.__send_cmd("remote_cmd",  "music:" + in_objects[1] ) 
                 res = "playing music"
 
            elif in_objects[0] =="image": 
                img = "./assets/cinder.jpg"
                if len(in_objects)  > 1:
                    img = in_objects[1]
                image = Image.open(img)
                image.show() 

        return  ""  
