from emtables.tables import EMTable
from emtables.ics_EDXS import ElectronIonization
from emtables.ics_EDXS.EDXS_sdicts import create_transition_dict, create_shell_dict, create_line_dict
import xraylib as xr

class EDXSTable (EMTable) : 
    def __init__ (self, cs_threshold = 1e-25, beam_energy = 200, energy_range = 20, **kwargs) :
        super().__init__(**kwargs)
        try :
            self.energy_start = energy_range[0]
            self.energy_end = energy_range[1]
        except TypeError :
            self.energy_start = 0
            self.energy_end = energy_range
        self.beam_energy = beam_energy
        self.cs_threshold = cs_threshold
        
        self.mdata["beam_energy"] = beam_energy
        self.mdata["energy_start"] = self.energy_start
        self.mdata["energy_end"] = self.energy_end
        self.mdata["cs_threshold"] = cs_threshold
        self.mdata["type"] =  "EM_EDXS_Xrays"
        
        
    def generate_table (self,lines = False) :
        element_dict = {}
        shell_dict = create_shell_dict()
        line_dict = create_line_dict()
        self.mdata["lines"] = lines
        for elt in self.elements : 
            ics = ElectronIonization(elt,self.beam_energy)
            ics.calc_ionization()
            i_dict = ics.i_dict
            lines_dict = {}
            quant_dict = {}
            energies = []
            ratios = []
            for shell in i_dict.keys():
                trans_dict = create_transition_dict(shell,line_dict)
                for line in trans_dict.keys():
                    # Not all the shell and line combination are valid. They need to be checked for validity first
                    try:
                        ratio = (
                            i_dict[shell]
                            * xr.FluorYield(elt, shell_dict[shell])
                            * xr.RadRate(elt, trans_dict[line])
                        )

                        energy = xr.LineEnergy(elt, trans_dict[line])
                        # There is no need to included the undetected lines as well as the minor ones
                        if (energy > self.energy_start) and (energy < self.energy_end)\
                        and (ratio > self.cs_threshold) and (energy < self.beam_energy):
                            if lines : 
                                lines_dict[line] = {"energy" : energy,"cs" : ratio}
                            else : 
                                ratios.append(ratio)
                                energies.append(energy)
                    # if a shell line is rejected we go to the next one.
                    except ValueError:
                        pass
            if lines : 
                if not (lines_dict == {}) : 
                    element_dict[str(elt)] = lines_dict
            else : 
                # Some shells are empty, especially for light elements. We need to exclude that case.
                if not (ratios == []):
                    element_dict[str(elt)] = {"energies" : energies, "cs" : ratios}
        self.table = element_dict
        
if __name__ == "__main__" :
    t = EDXSTable(elements = [26],beam_energy = 200, energy_range = 20)
    t.generate_table(lines = True)
    print(t.table)
    ask = input("Generate the default table (This will take a while) ? [y|n]")
    if ask == "y" : 
        t = EDXSTable()
        t.generate_table()
        t.save_table("default_xrays.json")