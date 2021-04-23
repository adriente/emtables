import xraylib as xr
import os
import pandas as pd
import numpy as np
import re
from emtables.ics_EDXS.EDXS_sdicts import create_shell_dict,create_line_dict, create_transition_dict, create_auger_dict
from emtables.conf import LOW_OV_FILE, HIGH_OV_FILE, BR_CONST

class ElectronIonization () : 
    def __init__ (self, element, beam_energy=200) :
        self.low_OV_table = pd.read_fwf(LOW_OV_FILE).fillna(method="ffill")
        self.high_OV_table = pd.read_fwf(HIGH_OV_FILE).fillna(method="ffill")
        self.element = element
        self.beam_energy = beam_energy
        self.shell_dict = create_shell_dict()
        self.line_dict = create_line_dict()
        self.i_dict = self.initialize_ionization()
        
        
    def initialize_ionization (self) :
        fi_dict = {}
        for key in self.shell_dict.keys() :
            try :
                fi_dict[key] = self.first_ionization(key)
            except ValueError :
                pass
        return fi_dict
        
    def calc_ionization (self) : 
        shell_list = list(self.i_dict.keys())
        shell_list.sort()
        for key in shell_list : 
            cs = self.i_dict[key]
            cs += self.rad_ionization(key)
            cs += self.full_auger_ionization(key)
            cs += self.CK_ionization(key)
            
            self.i_dict[key] = cs

    def get_idict(self,shell) :
        try :
            value = self.i_dict[shell]
            return value
        except KeyError as exc :
            raise ValueError("Beam energy too low for shell excitation") from exc
        
    def first_ionization(self,shell):
        """
        Calculates the first ionization cross-section of the given shell of the given element using the Bote 2009 tables. These table are only valid for ionization of atoms by electrons.
        :element: integer
        :shell: Shell string
        """
        # Tries first to get the ionization energy if possible for the given shell and element
        if self.beam_energy < xr.EdgeEnergy(self.element,self.shell_dict[shell]) :
            raise ValueError("Beam energy not high high enough to excite the {} shell".format(shell))
        else :
            try:
                energy = self.low_OV_table.loc[
                    (self.low_OV_table["Z"] == self.element) & (self.low_OV_table["S"] == shell)
                ].iloc[0]["E"]
                U = self.beam_energy * 1000 / energy
                # There are two analytical
                if U < 16:
                    # Full expression of the cross section for low OV : 4*pi*a0**2*(U-1)/(U**2)*(a1 + a2*U + a3/(1+U) + a4/(1+U)**3 + a5/(1+U)**5)
                    # Useful expression of X-ray ratios : (a1 + a2*U + a3/(1+U) + a4/(1+U)**3 + a5/(1+U)**5)
                    # U is OverVoltage (OV) and a0 is the Bohr radius
                    a_values = self.low_OV_table.loc[
                        (self.low_OV_table["Z"] == self.element)
                        & (self.low_OV_table["S"] == shell)
                    ]
                    a1 = a_values["a1"].iloc[0]
                    a2 = a_values["a2"].iloc[0]
                    a3 = a_values["a3"].iloc[0]
                    a4 = a_values["a4"].iloc[0]
                    a5 = a_values["a5"].iloc[0]
                    cs = BR_CONST*(
                        (U-1)/np.power(U,2)*
                        np.power((a1
                        + a2 * U
                        + a3 / (1 + U)
                        + a4 / ((1 + U) ** 3)
                        + a5 / ((1 + U) ** 5)),2)
                    )
                else:
                    # Full expression of the cross section for high OV :
                    # Eb/(Eb + b*Ek)*4*pi*a0**2*A/B**2 *((ln(X**2)-B**2)*(1+g1/X) + g2 + g3*(1-B**2)**(-1/4) + g4/X)
                    param_values = self.high_OV_table.loc[
                        (self.high_OV_table["Z"] == self.element)
                        & (self.high_OV_table["S"] == shell)
                    ]
                    me = 511000  # electron rest mass in eV
                    beam_ev = self.beam_energy * 1000
                    B = np.sqrt(beam_ev * (beam_ev + 2 * me)) / (beam_ev + me)
                    X = np.sqrt(beam_ev * (beam_ev + 2 * me)) / me
                    b_ = param_values["b-"].iloc[0]
                    A = param_values["Anlj"].iloc[0]
                    g1 = param_values["g1"].iloc[0]
                    g2 = param_values["g2"].iloc[0]
                    g3 = param_values["g3"].iloc[0]
                    g4 = param_values["g4"].iloc[0]
                    cs = BR_CONST*(
                        U/ (U + b_)
                        * A / np.power(B,2)
                        * (
                            (np.log(np.power(X, 2)) - B ** 2) * (1 + g1 / X)
                            + g2
                            + g3 * np.power((1 - B ** 2), -0.25)
                            + g4 / X
                        )
                    )

                return cs
            # returns the same error as the xraylib to have homogeneous execptions
            except IndexError as exc:
                raise ValueError("first ionization : wrong shell") from exc

    def full_auger_ionization (self,shell) :
        cs = 0
        shell_list = list(self.shell_dict.keys())
        shell_list.sort()
        for i in range(shell_list.index(shell)) :
            cs += self.auger_ionization(shell,shell_list[i])
        return cs
           
    def CK_ionization (self,shell) :
        # For the L1, there is not coster kronig
        # For the higher shells there are transitions from the lower shells added too
        cs = 0
        regex = r"([K-M])([0-9]?)"
        shell_group = re.match(regex,shell).group(1)
        if shell_group != "K" :
            for i in range(1, int(shell[1])):
                try:
                    string_CK = "F{}{}{}_TRANS".format(shell_group,i, shell[1])
                    string_shell = shell_group + "{}".format(i)
                    cs += self.get_idict(string_shell) * xr.CosKronTransProb(self.element, xr.__dict__[string_CK])
                except ValueError:
                    pass
        return cs
        
    def rad_ionization (self,shell) :
        regex = r"([K-M])([0-9]?)"
        cs = 0
        for key in self.shell_dict.keys() :
            shell_group = re.match(regex,shell).group(1)
            key_group = re.match(regex,key).group(1)
            if shell_group > key_group :
                tr_dict = create_transition_dict(key,self.line_dict)
                try : 
                    fy = xr.FluorYield(self.element,self.shell_dict[key])
                    rr = xr.RadRate(self.element,tr_dict[key + shell])
                    key_i = self.get_idict(key)
                    cs+= key_i * fy * rr
                except ValueError :
                    pass
        return cs

    def auger_ionization (self,shell,lower_shell) :
        if shell == "K" :
            return 0
        else : 
            auger_dict = create_auger_dict(shell,lower_shell)
            try : 
                fi = self.get_idict(lower_shell)
                ay = xr.AugerYield(self.element,self.shell_dict[lower_shell])
                ar = 0
                for trans in auger_dict.keys() : 
                    try :
                        ar += xr.AugerRate(self.element,auger_dict[trans])
                    except ValueError :
                        pass
                return fi*ar*ay
            except ValueError :
                return 0

if __name__ == "__main__" :
    a = ElectronIonization(79,3)
    print("Before corrections : ",a.i_dict)
    a.calc_ionization()
    print("After corrections : ",a.i_dict)