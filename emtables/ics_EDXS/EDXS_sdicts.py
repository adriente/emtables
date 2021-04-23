import re
import xraylib as xr

def create_shell_dict():
    """
    Creation of the internal dict which stores every SHELL macro from the xraylib.
    The dict has this structure : {"Shell name": int}
    """
    re_shell = r"([K-M][0-9]?)(_SHELL)"
    shell_dict = {}
    for key in xr.__dict__.keys():
        shell = re.match(re_shell, key)
        if shell:
            shell_dict[shell.group(1)] = xr.__dict__[key]
    return shell_dict

def create_line_dict():
    """
    Creation of the internal dict which stores every LINE macro from the xraylib.
    The dict has this structure : {"Line name": int}
    """
    re_line = r"([A-Z][0-9]?[A-Z][0-9])(_LINE)"
    line_dict = {}
    for key in xr.__dict__.keys():
        line = re.match(re_line, key)
        if line:
            line_dict[line.group(1)] = xr.__dict__[key]
    return line_dict

def create_transition_dict(shell, line_dict):
    """
    Generates a dictionary of the lines associated with the given shell.
    The dict has this structure : {"line_name":int}
    """
    transition_dict = {}
    regex = shell + r"[H-Z][0-9]"
    for line in line_dict.keys():
        if re.match(regex, line):
            transition_dict[line] = line_dict[line]
    return transition_dict
    
def create_auger_dict(shell, lower_shell) :
    auger_dict = {}
    regex = lower_shell + "_" + shell + r"([H-Z][0-9])_AUGER"
    for tr in xr.__dict__.keys() :
        if re.match(regex, tr) :
            auger_dict[tr] = xr.__dict__[tr]
    return auger_dict



