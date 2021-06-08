from emtables.tables import EMTable
from emtables.conf import PERIODIC_TABLE_FILE
import json

class ElementsTable (EMTable) :
    def __init__(self,**kwargs) : 
        super().__init__(**kwargs)
        with open(PERIODIC_TABLE_FILE,"r") as f : 
            self.periodic_table = json.load(f)["elements"]
        
    def generate_table (self,symbols = False) :
        for i,elt in enumerate(self.periodic_table) :
            elt_dict = {}
            if (i+1) in self.elements :
                elt_dict["atomic_mass"] = self.periodic_table[i]["atomic_mass"]
                elt_dict["density"] = self.periodic_table[i]["density"]
                if symbols : 
                    elt_dict["number"] = self.periodic_table[i]["number"]
                    self.table[self.periodic_table[i]["symbol"]] = elt_dict
                    self.mdata["type"] =  "Periodic table : Symbols"
                else : 
                    elt_dict["symbol"] = self.periodic_table[i]["symbol"]
                    self.table[self.periodic_table[i]["number"]] = elt_dict
                    self.mdata["type"] =  "Periodic table : Number"
                
if __name__ == "__main__" : 
    t = ElementsTable(elements = [27])
    t.generate_table(symbols=True)
    print(t.table)
    ask = input("Generate the 2 default table (This will take a while) ? [y|n]")
    if ask == "y" : 
        t1 = ElementsTable()
        t1.generate_table(symbols = True)
        t1.save_table("periodic_table_symbols.json")
        t2 = ElementsTable()
        t2.generate_table(symbols = False)
        t2.save_table("periodic_table_number.json")
                
    