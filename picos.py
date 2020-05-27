from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

def pico(wave,flux,avance=10):
    """
    Pico
    ====
    Esta función saca los maximos y minimos del espectrograma, a partir de una
    longitud de onda, y una luminosidad (del mismo tamaño). Nos devuelve dos 
    arrays, uno de máximos y otro de mínimos. Además plotea la función
    normalizada y los puntos máximos y mínimos

    Parameters
    ----------
    -wave: array de la longitud de onda de nuestro espectro

    -flux: array de la luminosidad de nuestro espectro

    -Avance: este parámetro determina que no haya un maximo/mínimo mayor/menor 
    que el potencial pico analizado en cada momento por la función. Si se pone
    un mayor valor se saltará algunos picos que pueden ser o no útiles en nuestro
    análisis.

    Returns
    ---------
    Array de máximos y mínimos

    """
    # Errores
    if wave.shape != flux.shape:
        raise Exception("Los arrays de longitud de onda y de luminosidad deben tener el mismo tamaño")

    maximo,minimo = 1.0,1.0
    listaMaximos, listaMinimos = [], []
    posmax,posmin = 0,0

    # Delta es un filtro para el ruido en el eje Y para el calculo de picos. Es la diferencia que tiene
    #  que haber entre un pico y el siguiente posible máximo.
    delta = (max(flux)-min(flux))/4


    for i, (x,y) in enumerate(zip(wave[:], flux[:])):
        # Potencial máximo
        if y > maximo:
            maximo = y
            posmax = x
        # Potencial mínimo
        if y < minimo:
            minimo = y
            posmin = x

        # Análisis de Potencial máximo
        if y < maximo-delta and maximo > 1.02:
            if flux[i:i+avance].max() < maximo:
                listaMaximos.append((posmax,maximo))
                maximo = 1.0

        if y > minimo+delta and 0.98 > minimo:
            if flux[i:i+avance].max() > minimo:
                listaMinimos.append((posmin,minimo))
                minimo = 1.0

    arrayMaximos, arrayMinimos = np.zeros((2,len(listaMaximos))), np.zeros((2,len(listaMinimos)))

    index = 0
    for i in listaMaximos:
        arrayMaximos[:,index] = i
        index = index + 1

    index = 0
    for i in listaMinimos:
        arrayMinimos[:,index] = i
        index = index + 1

    plt.plot(wave,flux,'k-', lw=0.3)
    plt.plot(arrayMinimos[0,:],arrayMinimos[1,:],'ro')
    plt.plot(arrayMaximos[0,:],arrayMaximos[1,:],'bo')
    plt.show()
    return listaMinimos, arrayMinimos