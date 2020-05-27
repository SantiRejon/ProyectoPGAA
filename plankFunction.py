import numpy as np
from scipy import constants as cons
from math import exp
import pylab as plt


def plank(wavelenght,Temperatura):
    """
    Plank
    =====

    La función usa la función de Plank para calcular el espectro de cuerpo oscuro del
    espectrograma a partir de su temperatura y un array de longitud de onda.

    Parameters
    ----------
    -wavelenght: array con las longitudes de onda del espectrograma (en micrómetros)

    -Temperatura: temperatura de la estrella (en Kelvins).

    Returns
    -------
    -Array de con la luminosidad del espectro de cuerpo oscuro.
    """
    
    wave = wavelenght*10**-10
    B = np.zeros_like((wavelenght))
    I = np.zeros_like((wavelenght))
    a = 2.0*cons.h*cons.pi*cons.c**2
    emissivity = 0.98
    temp = Temperatura/emissivity
    
    for i,w in enumerate(wave[:]):
            B[i] = cons.h*cons.c/(w*cons.k*Temperatura)
            I[i] = emissivity * a / ((w**5)*(exp(B[i])-1.0))*10**-14
    
    return I
