import pylab as plt
from scipy.interpolate import splrep,splev
import numpy as np
from scipy.signal import medfilt
from plankFunction import plank


def normaliza(wave,flux):

    """
    Normaliza
    =====
    La función hace un ploteo interactivo de wave (eje x) y flux (eje y). En ese ploteo se pueden marcar
    puntos que conformarán el continuum de nuestro espectro, normalizar el espectro a partir del continuum
    y guardar en un archivo txt los datos del eje x e y del espectrograma normalizado

    Parameters
    ----------
    -wave: array de la longitud de onda de nuestro espectro

    -flux: array de la luminosidad de nuestro espectro

    Returns
    ----------
    Archivo .txt con los datos de longitud de onda y luminosidad

    Notes
    ---------
    Estos arrays deben ser del mismo tamaño.

    """
    if wave.shape != flux.shape:
        raise Exception("Los arrays de longitud de onda y de luminosidad deben tener el mismo tamaño")

    def onclick(event):
        """
        Donde el usuario haga click con el boton izquierdo del raton, 
        se ploteara un pto del continuum de su eleccion. 

        El tamaño del punto esta determinado por ms.

        Picker es un parámetro de área que se usa en la función onpick
        """
        if event.button==1:
            plt.plot(event.xdata,event.ydata,'r.',ms=10,picker=5,label='nuevoPunto')
        plt.draw()

        
    def onpick(event):
        """
        Si el usuario hace click con el boton derecho del raton
        cerca (rango determinado por el parámetro picker de onclick) 
        de un punto creado anteriormente, se eliminará el mismo 
        (o los que estén en el rango)
        
        """
        if event.mouseevent.button==3:
            if hasattr(event.artist,'get_label') and event.artist.get_label()=='nuevoPunto':
                event.artist.remove()

    def ontype(event):
        """
        Cuando el usuario pulse "enter" tras haber seleccionado los puntos
        deseados de continuum, se creará un spline de tercer grado que representa
        el continuum. Se pueden añadir más puntos después y al volver a pulsar 
        "enter" se actualizará el spline.

        Cuando pulse "n" se realizará la normalización respecto del spline o continuum.

        Si pulsa "g" los valores de Luminosidad relativa y longitud de onda se guardarán en un
        archivo .txt de nombre normalizacion.

        Si pulsa "r" se volverá a la forma original del espectro eliminando los puntos y spline.

        Si pulsa "a" el programa hace la normalización automáticamente, sun necesidad de crear
        manualmente el continuum.

        Si pulsa "t" el programa realiza la normalización de forma teórica con la función de Plank
        para cuerpos oscuros.

        """

        # Ploteo Continuum
        if event.key=='enter':
            new_pto_coord = []
            for artist in plt.gca().get_children():
                if hasattr(artist,'get_label') and artist.get_label()=='nuevoPunto':
                    new_pto_coord.append(artist.get_data())
                elif hasattr(artist,'get_label') and artist.get_label()=='continuum':
                    artist.remove()
            new_pto_coord = np.array(new_pto_coord)[...,0]
            sort_array = np.argsort(new_pto_coord[:,0])
            x,y = new_pto_coord[sort_array].T
            spline = splrep(x,y,k=3)
            continuum = splev(wave,spline)
            plt.plot(wave,continuum,'r-',lw=2,label='continuum')

        # Temperatura de la estrella. Obtenida con la Ley de Wien para cuerpos negros
            max_lux = np.amax(continuum)
            wave_index_max = np.where(continuum == np.amax(continuum))

            temperatura = 29000000.0/float(wave[wave_index_max])
            print("Temperatura aproximada de la estrella (K) =",temperatura)
            


        # Normalizacion
        elif event.key=='n':
            continuum = None
            for artist in plt.gca().get_children():
                if hasattr(artist,'get_label') and artist.get_label()=='continuum':
                    continuum = artist.get_data()[1]
                    break
            if continuum is not None:
                plt.cla()
                plt.plot(wave,flux/continuum,'k-',label='normalizacion', lw=0.3)
            
            # Guardado de "seguridad" por si el usuario no guarda la normalización
            for artist in plt.gca().get_children():
                if hasattr(artist,'get_label') and artist.get_label()=='normalizacion':
                    datos_normalizar = np.array(artist.get_data())
                    np.savetxt("normalizacion.txt",datos_normalizar.T)
                    break

        # Normalizado Teórico
        elif event.key == 't':
            data = np.zeros_like((wave,flux))
            data[0,:],data[1,:] = flux, wave
            auxList = []


            # Temperatura de la estrella. Obtenida con la Ley de Wien para cuerpos negros
            pseudocontinuum = medfilt(data[0,:],301)
            pseudocontinuumNoError = pseudocontinuum [50:-50]
            max_lux = max(pseudocontinuum)
            wave_index_max = np.amin(np.where(pseudocontinuum == max_lux))
            wave_max = data[1,wave_index_max]
            temperatura = 29000000.0/float(wave_max)
            print("Temperatura aproximada de la estrella (K) =",temperatura)


            # Obtención del espectro de cuerpo oscuro y noramliación de la función.
            continuum = plank(data[1,:],temperatura-100)
            continuum_noError = continuum [50:-50]
            normData = data[0,50:-50]/pseudocontinuumNoError
            plt.cla()
            plt.plot(data[1,50:-50],normData,'k-',lw=0.3, label='normalizacion')

            
            # Guardado de "seguridad" por si el usuario no guarda la normalización
            for artist in plt.gca().get_children():
                if hasattr(artist,'get_label') and artist.get_label()=='normalizacion':
                    datos_normalizar = np.array(artist.get_data())
                    np.savetxt("normalizacion.txt",datos_normalizar.T)
                    break


        # Normalizado Automático
        elif event.key == 'a':
            data = np.zeros_like((wave,flux))
            data[0,:],data[1,:] = flux, wave
            auxList = []
 
            pseudocontinuum = medfilt(data[0,:],301)+0.06
            pseudocontinuumNoError = pseudocontinuum [50:-50]
            normData = data[0,50:-50]/pseudocontinuumNoError
            plt.cla()
            plt.plot(data[1,50:-50],normData,'k-',lw=0.3, label='normalizacion')

            # Temperatura de la estrella. Obtenida con la Ley de Wien para cuerpos negros
            max_lux = max(pseudocontinuum)
            wave_index_max = np.amin(np.where(pseudocontinuum == max_lux))
            wave_max = data[1,wave_index_max]
            temperatura = 29000000.0/float(wave_max)
            print("Temperatura aproximada de la estrella (K) =",temperatura)


            
            # Guardado de "seguridad" por si el usuario no guarda la normalización
            for artist in plt.gca().get_children():
                if hasattr(artist,'get_label') and artist.get_label()=='normalizacion':
                    datos_normalizar = np.array(artist.get_data())
                    np.savetxt("normalizacion.txt",datos_normalizar.T)
                    break


        # Guardado del espectrograma normalizado.
        elif event.key=='g':
            for artist in plt.gca().get_children():
                if hasattr(artist,'get_label') and artist.get_label()=='normalizacion':
                    datos_normalizar = np.array(artist.get_data())
                    np.savetxt("normalizacion.txt",datos_normalizar.T)
                    print('Se ha guardado la normalización en el archivo normalizacion.txt')
                    break

        # Reinicio del proceso, vuelve a plotear el espectrograma original
        elif event.key=='r':
            plt.cla()
            plt.plot(wave,flux,'k-',lw=0.3)

        plt.draw()


    #Conectamos las funciones interactivas con sus respectivos eventos

    plt.gcf().canvas.mpl_connect('key_press_event',ontype)
    plt.gcf().canvas.mpl_connect('button_press_event',onclick)
    plt.gcf().canvas.mpl_connect('pick_event',onpick)

    spectrum = plt.plot(wave,flux,'k-', lw=0.3)
    plt.show()

    return

        
    
    

