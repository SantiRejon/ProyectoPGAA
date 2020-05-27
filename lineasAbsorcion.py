import numpy as np


def linea(arrayMinimos,linea):
    """
    Linea
    =====

    Esta funcion se encarga de reconocer qué líneas de absorción presenta el espectrograma contemplado.
    Para cada línea de absorción la función selecciona la frecuencia correspondiente
    y comprueba si previamente hemos encontraado un pico en el rango de frecuencias en el que se encontraría la línea.
    Si la encuentra, devuelve la intensidad de la línea pedida.

    Parameters
    ==========
    -arrayMinimos: array con los mínimos del espectrograma.
    -linea: string con el nombre de la linea a buscar.

    Returns
    =======
    -haylinea: booleano con true si la linea existe
    -intensidadPico: la intensidad del pico de esa línea.

    Observations
    ============
    Las lineas de absorcion implementadas son 'Balmer', 'FraunhoferK', 'FraunhoferH', 'GBand', 'ManganMn', 'Titanoxide' and 'FeI'
    """
    
    precision = 2.6 # La librería tiene una precisión de 2.6 Armstrong

    #Establecemos la longitud de onda de las diferentes líneas implementadas para búsqueda.

    if linea == 'Balmer':
        wavelength = 4341.0
    elif linea == 'FraunhoferK':
        wavelength = 3934.0
    elif linea == 'FraunhoferH':
        wavelength = 3968.0
    elif linea == 'GBand':
        wavelength1 = 4300.0
        wavelength2 = 4310.0
    elif linea == 'ManganMn':
        wavelength1 = 4031.0
        wavelength2 = 4036.0
    elif linea == 'Titanoxide':
        wavelength1 = 5168.0
        wavelength2 = 5172.0
    elif linea == 'FeI':
        wavelength = 4325.0

    hayLinea = False
    intensidadPico = 0

    #Detectamos si para esa longitud de onda existe una línea de mínimo en el espectrograma normalizado.

    if linea == 'ManganMn' or linea == 'Titanoxide' or linea == 'GBand':
        rango = list(np.arange(wavelength1-precision, wavelength1+precision, 0.1)) + list(np.arange(wavelength2-precision, wavelength2+precision, 0.1))
        rango = np.around(np.array(rango),1)
    elif linea == 'GBand':
        rango = np.around(np.arange(wavelength1, wavelength2, 0.1), 1)
    else:
        rango = np.around(np.arange(wavelength-(precision), wavelength+(precision), 0.1), 1)
    for i in rango:
        if i in arrayMinimos[0,:]:
            hayLinea = True
            intensidadPico = 1 - arrayMinimos[1,(np.where(arrayMinimos[0,:] == i))]
        else:
                pass

    return hayLinea, intensidadPico
