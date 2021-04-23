import numpy as np

def wernisch_dK(Z):
    return (
        5.955
        + 3.917e-1 * Z
        - 1.054e-2 * np.power(Z, 2)
        + 1.520e-4 * np.power(Z, 3)
        - 8.508e-7 * np.power(Z, 4)
    )

def wernisch_dL(Z):
    return (
        3.257
        + 3.936e-1 * Z
        - 8.483e-3 * np.power(Z, 2)
        + 9.491e-5 * np.power(Z, 3)
        - 4.058e-7 * np.power(Z, 4)
    )

def wernisch_dM(Z):
    return (
        2.382 + 2.212e-1 * Z - 2.028e-3 * np.power(Z, 2) + 6.891e-6 * np.power(Z, 3)
    )

def wernisch_dN(Z):
    return 4.838 + 4.911e-2 * Z