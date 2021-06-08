from abc import ABC, abstractmethod 
import json

class EMTable (ABC) : 
    def __init__(self,elements = 99) :
        
        try : 
            self.elements = range(elements)
        except TypeError :
            self.elements = elements
        
        self.table = {}
        self.mdata = {}
        
    @abstractmethod
    def generate_table(self) :
        pass
        
    def save_table(self,filename) :
        save_dict = {"table" : self.table, "metadata" : self.mdata}
        with open(filename, "w") as f:
            json.dump(save_dict, f, indent=4)