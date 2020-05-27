import numpy as np 
from astropy.io import fits


def lectorFits(rutaEspectrograma):
    """
    lectorFits
    ==========
    La función lee un archivo de tipo fits. Plotea el HDU, el Header del archivo (para que el usuario compruebe
    las filas de datos), el tamaño del array de datos, y saca dos archivos txt con la longitud de onda y la luminosidad y 
    un dos array, uno de longitud de onda y otro de luminosidad.

    Parameters
    ----------
    -rutaEspectrograma: string con el nombre de la ruta del archivo fits. Si es un array con más de una fila
    de datos, es importante revisar que la función escriba correctamente en la variable el dato que queremos
    sacar

    Returns
    -------
    -Dos archivos txt, uno con la longitud de onda y otro con la luminosidad.
    
    -Dos arrays, uno con la longitud de onda y otro con la luminosidad.
    """
    archivoFits = fits.open(rutaEspectrograma)
    archivoFits.info()

    # Extraemos el Header del FITS
    # Selecionamos [0] porque en el ejemplo el PRIMARY del HDU esta en el 0. El primary en los archivos FITS
    # es el array que contiene los datos principales.

    head=archivoFits[0].header
    print(repr(head))
    print(archivoFits[0].data.shape)

    # Extraemos los datos del FITS y asignamos la longitud de onda
    dataEspec = np.zeros((2,len(archivoFits[0].data[0,:])))

    # Cada pixel del espectrograma son 0.9 angstroms
    wave = []
    for i in range(len(dataEspec[0,:])):
            wave.append(3500.0+(i*0.9))

    wave = np.array(wave)
    wave.round(2)

    dataEspec[0,:] = wave
    dataEspec[1,:] = archivoFits[0].data[0,:]

    # Recortamos error de principio y final
    data = np.zeros((2,len(dataEspec[0,:])-150))
    data[0,:] = dataEspec[0,75:-75]
    data[1,:] = dataEspec[1,75:-75]

    # Obtenemos los archivos TXT.
    file = np.savetxt("wavelength.txt",data[0,:])
    file = np.savetxt("flux.txt",data[1,:])

    archivoFits.close()

    wavelenght = data[0,:]
    flux = data[1,:]

    return wavelenght, flux
