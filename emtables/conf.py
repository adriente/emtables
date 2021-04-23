from pathlib import Path
import numpy as np

# Path of the base
BASE_PATH = Path(__file__).parent

# Path of the db
DB_PATH = BASE_PATH / Path("Data/")

LOW_OV_FILE = DB_PATH / Path("Bote2009_lowOV.txt")
HIGH_OV_FILE = DB_PATH / Path("Bote2009_highOV.txt")

#In cm2
BOHR_RADIUS = 5.291772109e-9
BR_CONST = 4*np.pi*np.power(BOHR_RADIUS,2)