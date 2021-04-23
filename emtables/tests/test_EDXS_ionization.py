import emtables.ics_EDXS.EDXS_ionization as Ei
import xraylib as xr
import numpy as np

def test_init () :
    ics = Ei.ElectronIonization(26)
    init_dict = ics.i_dict
    shell_list = ["K","L1","L2","L3","M1","M2","M3"]
    assert list(init_dict.keys()) == shell_list
    
def test_CK_ionization () :
    ics = Ei.ElectronIonization(26)
    
    CK_cs_1 = ics.CK_ionization("L2")
    CK_cs_2 = ics.i_dict["L1"] * xr.CosKronTransProb(26, xr.__dict__["FL12_TRANS"])
    assert CK_cs_1 == CK_cs_2
    
    CK_cs_K = ics.CK_ionization("K")
    assert CK_cs_K == 0
    
def test_rad_ionization () :
    ics = Ei.ElectronIonization(26)
    
    L3_cs_1 = ics.rad_ionization("L3")
    L3_cs_2 = ics.i_dict["K"] * xr.FluorYield(26,xr.__dict__["K_SHELL"]) * xr.RadRate(26,xr.__dict__["KL3_LINE"])
    assert L3_cs_1 == L3_cs_2
    
    L1_cs_1 = ics.rad_ionization("L1")
    assert L1_cs_1 == 0
    
def test_auger_ionization () :
    ics = Ei.ElectronIonization(26)
    
    auger_cs_1 = ics.auger_ionization("L1","K")
    auger_temp = 0
    for i in range(30) :
        try :
            auger_temp += xr.AugerRate(26,i)
        except ValueError :
            pass
    auger_cs_2 = auger_temp * xr.AugerYield(26,xr.__dict__["K_SHELL"]) * ics.i_dict["K"]
    np.testing.assert_allclose(auger_cs_1, auger_cs_2)
    
    auger_cs_K = ics.auger_ionization("K","K")
    assert auger_cs_K == 0
    
    full_auger_1 = ics.full_auger_ionization("L2")
    auger_rates_K = 0
    for i in range(30,60) :
        try :
            auger_rates_K += xr.AugerRate(26,i)
        except ValueError :
            pass
    auger_cs_K = auger_rates_K*xr.AugerYield(26,xr.__dict__["K_SHELL"]) * ics.i_dict["K"]
    auger_rates_L1 = 0
    for i in range(240,269) :
        try :
            auger_rates_L1 += xr.AugerRate(26,i)
        except ValueError :
            pass
    full_auger_2 = auger_cs_K + auger_rates_L1*xr.AugerYield(26,xr.__dict__["L1_SHELL"]) * ics.i_dict["L1"]        
    np.testing.assert_allclose(full_auger_1, full_auger_2)
    

            
            
            
            
            