from pathlib import Path
import numpy as np

# Path of the base
BASE_PATH = Path(__file__).parent

# Path of the db
DB_PATH = BASE_PATH / Path("Data/")

PERIODIC_TABLE_FILE = DB_PATH / Path("Periodic-Table-JSON/PeriodicTableJSON.json")

LOW_OV_FILE = DB_PATH / Path("Bote2009_lowOV.txt")
HIGH_OV_FILE = DB_PATH / Path("Bote2009_highOV.txt")

#In cm2
BOHR_RADIUS = 5.291772109e-9
BR_CONST = 4*np.pi*np.power(BOHR_RADIUS,2)

WERNISCH_H = {
            "L1": 1,
            "L2": 0.862,
            "L3": 0.611,
            "M1": 1,
            "M2": 0.935,
            "M3": 0.842,
            "M4": 0.638,
            "M5": 0.443,
        }