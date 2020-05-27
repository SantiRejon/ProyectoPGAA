---------------------------------------------------------------------------
            Tratado de espectrogramas y clasificación estelar
---------------------------------------------------------------------------

Este programa está pensado para trabajar con la librería MILES v9.5, 
cuyos ficheros .fits están descargados de
http://research.iac.es/proyecto/miles/media/tarfiles/Stellar_Libraries/MILES_library_v9.1_FITS.tar.gz


Para usar el programa:

1. Especificar la ruta del archivo .fits que se quiere analizar en main.py

2. Al ejecutar main.py, el programa leerá el .fits y representará el espectrograma.
Desde aquí el usuario tiene varias opciones:

3.1. Si se pulsa la tecla 't', el programa hallará el continuum teórico del espectrograma y lo normalizará.

3.2. Si se pulsa la tecla 'a', el programa normalizará la función de forma automática y la representará.

3.2. Para normalizar la función de manera manual, haciendo click izquierdo en la gráfica se definen puntos 
     pertenecientes al continuum.
	- Se pueden borrar puntos que no queramos haciendo click derecho en ellos.
	- Una vez se considere que hay puntos suficientes, se pulsa la tecla enter para generar un 
	  spline que será el continuum utilizado para normalizar.
	- Una vez definido el spline, pulsando la tecla 'n', el programa normaliza la función y la representa.
	- Si desde aquí se quiere volver a la gráfica original para cambiar el continuum se puede hacer 
	  pulsando 'r'.

4. Después del normalizado, el programa hallará los picos de la función, que servirán para encontrar
   las líneas de absorción y/o emisión del espectrograma.

5. El programa clasificará la estrella según la clasificación Harvard en base a las líneas encontradas.


