from lectorFits import lectorFits
import pylab as plt
from normalizar import normaliza
import numpy as np
from picos import pico
from clasificacion import Harvard


if __name__ == "__main__":

    #Ruta del archivo
    archivo = 'MILES_library_v9.1_FITS/s0019.fits'

    # Obtenemos la longitud de onda y su respectiva luminosidad del archivo FITS
    wave, flux = lectorFits(archivo)

    #Ploteo del espectro (sin representarlo)
    spectrum = plt.plot(wave,flux,'k-', lw=0.3)
    plt.title('Espectro de %s' %archivo)

    #Obtención del espectrograma normalizado
    normalizado = normaliza(wave,flux)
    print('Ha acabado la normalización')
    normalizacion = np.loadtxt("normalizacion.txt").T

    # plt.plot(normalizacion[0],normalizacion[1],'k-', lw=0.3)

    minimos,arrayMinimos = pico(normalizacion[0],normalizacion[1])

    clasif_estrella = Harvard(arrayMinimos)
    
    plt.show()


