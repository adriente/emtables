from abc import ABC, abstractmethod 
import json

class EMTable (ABC) : 
    def __init__(self,elements = 99, beam_energy = 200, energy_range = 20) :
        
        try : 
            self.elements = range(elements)
        except TypeError :
            self.elements = elements
        try :
            self.energy_start = energy_range[0]
            self.energy_end = energy_range[1]
        except TypeError :
            self.energy_start = 0
            self.energy_end = energy_range
        self.beam_energy = beam_energy
        self.table = {}
        self.mdata = {"beam_energy" : beam_energy,"energy_start" : self.energy_start,"energy_end" : self.energy_end}
        
    @abstractmethod
    def generate_table(self) :
        pass
        
    def save_table(self,filename) :
        save_dict = {"table" : self.table, "metadata" : self.mdata}
        with open(filename, "w") as f:
            json.dump(save_dict, f, indent=4)