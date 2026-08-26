#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: HipMonsters.com  
License: MIT License  
""" 
import threading
import datetime

def reminder(parent, message):
    """Function to display the reminder message."""
    parent.nerves.set("speech", message)
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Reminder: {message}")

from .utils.utils import dispatcher  ,replace_sep, split_ignoring_quotes
 
    
class  MiscTriples(object):
 
    def __init__(self:object):
        """
        Misc Functions
        
        """   
        pass
       

    @dispatcher
    def reminder(self: object, in_subjects:str= "", in_objects: str ="" )-> str:
        """
        Sets a reminder after a delay.
        """ 
        message, delay_seconds = in_subjects, int(in_objects)

        if delay_seconds < 0:
            raise ValueError("Delay must be non-negative.")
        timer = threading.Timer(delay_seconds, reminder, args=(self, message,))

        timer.daemon = True  # Daemon thread will exit when main program exits
        timer.start() 
        return f"Set reminder: {message}"
