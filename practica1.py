'''
@author: Diego Alejandro Toro Ramirez
'''

from jflap.Afd import Afd
import sys

'''CARGAR_AUTOMATA()
Crea un automata apartir de un fichero jff
El automata jff que se utilizará en esta práctica tiene 27 estados, dos de ellos fianales y correspondientes a la torre
correctamente montada en las agujas 2 y 3.
El minimo de movimientos para resolver el automata son 7 movimientos dada la formula 2^n-1 donde n es el numerod de discos
Dado esto, de la aguja 1 a la 2, para una torre valida, habran 7 estados
de la 2-3, para montar torre valida en la aguja 3, otros 7 estados (contando el ultimo que representa la aguja)
y de la 1-3, otros 7 estados.
Con esto tenemos el esqueleto del triangulo.
Para completar el interior, se uso  fuerza bruta probando
todas las combinaciones posibles de movimiento, asi como ciclos al mismo tiempo
que se usaba como  guia para la forma el Triángulo de Sierpinski
'''    
def cargar_automata():
    fichero = 'practica1.jff'
    return Afd(fichero)


'''ES_VALIDA
Este metodo sirve para validar una cadena dado un automata
esta basado en el algoritmo de validación visto en teoria.
Para ello:

        1º Obtiene el estado inicial del automata pasado como parametro
        
        2º Definimos una varible contador nEstado, dicha variable nos servirá en el metodo tratar_entrada() para determinar hasta que caracter
           de la cadena ha sido "tratada" por el automata (es decir hasta que posicion de la cadena ha podido "tratar" el automata pues cada transicion 
           supone la aceptación de un simbolo de la cadena de entrada) y para determinar en este metodo que simbolo de la cadena de entrada debemos tratar
           Mientras el nº de Estados transicionados sea menor que la longitud de la cadena :
           
               Observamos si existe una transición definida en el automata desde el estado actual para el siguiente simbolo de la cadena
               Si es asi entonces avanzo en el automata, asignando como estado actual el estado siguiente al que lleva la transicion 
               
               Si no existe la transicion devolvemos el nEstado, con lo cual indicaremos hasta que posición ha sido tratada la cadena,
               dicho valor será entonces siempre MENOR que la longuitud de la cadena indicando que la cadena no se ha leido entera y por tanto no es valida
           
        3º Si hemos tratado la cadena completa, entonces
            Si el estado actual es final entonces la Cadena es valida y devolvemos el nEstado, siendo este valor IGUAL a la longuitud de la cadena
            En caso contrario , la cadena no será valida, y entonces devolvemos nEstado + 1 , con lo cual al ser MAYOR que la longuitud de la cadena
            estaremos indicando que se ha leido entera pero no ha sido valida.


¡MUY IMPORTANTE OBSERVAR!

Hay que diferenciar bien entre la longuitud de la cadena 1-n
Y lo que podemos indexar 0 hasta n-1.

la cadena al ser un string, se trata desde 0 hasta n-1
para una correcta indexación. Por eso nEstado inicialmente es 0.
Sin embargo, la practica exige indicar la posicion desde 1 hasta n
Esta pequeña correccion se llevara acabo en el metodo tratar_entrada.

Hay que prestar atencion a la siguiente condicion:

if ( automata.estadoSiguiente(estadoActual, cadena[nEstado]) != None ):
            estadoActual = automata.estadoSiguiente(estadoActual, cadena[nEstado])
            nEstado += 1

En el caso de que las cadenas se lean enteras se trataran
0 hasta n-1, sin embargo nEstado tras leer el ultimo caracter no es n-1 si no n por  nEstado += 1
Luego si el estado es final, entonces se devolverá n
En caso contrario n+1, Y de esta forma sabremos en el metodo tratar_entrada si aun leyendo la cadena al completo es valida o no

El caso especial, es el que no se lea toda la cadena, en este caso

En la ultima iteración, no entrara por la condición y no se le sumará 1 estado, quedando el retorno
del rango 0 hasta n-1, cosa que seria incorrecta pues la salida debe ser desde 0-n.
Sin embargo no seria posible, sumarle 1 antes de devolver dicho nEstado, pues 
se podrian dar casos excepcionales en el que fallase en el que solo se tratase hasta el penultimo caracter,
dando como retorno al sumarle 1 que la cadena se ha leido entera de forma satisfactoria.

Por ello, para arreglar todo este lio, simplemente a las cadenas que no se traten completamente y por tanto no 
validas ( cuyo nEstado sea inferior a la longuitud de la cadena), tendremos que sumarle 1 justo antes de la salida por pantalla
para que cumpla con el formato del ejercicio y al mismo tiempo se pueda controlar


'''        
def es_valida(automata, cadena):
    estadoActual = automata.getEstadoInicial()
    nEstado=0
    
    while nEstado < len(cadena):
        #nEstado += 1 no lo podria poner aqui porq la indexacion seria incorrecta
        if ( automata.estadoSiguiente(estadoActual, cadena[nEstado]) != None ):
            estadoActual = automata.estadoSiguiente(estadoActual, cadena[nEstado])
            nEstado += 1 
        else:
            #nEstado += 1 tampoco puedo sumarlo aqui porque si se diese el caso de que fallase justamente en el antepenultimo estado seria correcto
            return nEstado 
          
    if(automata.esFinal(estadoActual)):
        return nEstado 
    else:
        return nEstado+1 

'''TRATAR_ENTRADA
En este metodo tratamos la entrada introducida por el usuario, para ello:
1º Intentamos abrir el fichero según el nombre del mismo introducido por usuario.
2º Si el fichero existe y se ha podido abrir:
    guardamos en un buffer, el contenido del mismo
3º Cargamos el automata  
   
4º Recorremos el buffer, Separando su contenido en lineas mediante rstrip() (las cuales estan delimitadas mediante saltos de linea)
    y obteniendo la cadena asociada a cada linea.
    Realizamos una llamada al metodo es_valida para obtener nEstado, el cual como explicamos más adelante
    nos sirve como "booleano" dado que si booleano es:
    
    IGUAL a la longuitud de la cadena -> entonces la cadena se ha leido de forma completa y es valida 
    MAYOR que la longuitud de la cadena -> entonces la cadena no será valida aunque se halla leido de forma completa
    MENOR que la longuitud de la cadena -> entonces la cadena no será valida, puesto que no se ha leido completamente,
    
    
5º Mostramos la salida formateada de todas las lineas, y una vez leidas todas , cerramos el fichero y volvemos a empezar la iteracion


Con respecto a las iteraciones comentar que el caso de que el fichero sea incorrecto, Se mostrara un mensaje por pantalla
Sin embargo, debido a que dicho mensaje esta tratado dentro de un try-catch y es fruto de una excepcion al abrir el fichero
Hay veces que la salida para la siguiente iteracion puede tener la forma

Fichero no encontrado o automata no disponible
Introduce el nombre del fichero con las cadenas a procesar >> 

Y otras veces

Introduce el nombre del fichero con las cadenas a procesar >> 
Fichero no encontrado o automata no disponible


'''
def tratar_entrada():
    iterar=True
    while(iterar):
        fichero = input('Introduce el nombre del fichero con las cadenas a procesar >> \n')
        if (fichero ==''):
            print('---Fin del programa----')
            break
        else:
            try:  
                fp = open(fichero)
                lineas = fp.readlines()
                automata = cargar_automata()
                n = 1
                for i in lineas:
                    cadena=i.rstrip()
                    booleano =es_valida(automata,cadena)
                    if( booleano == (len(cadena)) ):
                        print('Linea %d %s: valida' %(n,cadena))
                    elif ( booleano > (len(cadena)) ):
                        print('Linea %d %s: no valida en %d' %(n,cadena,booleano))
                    else:
                        print('Linea %d %s: no valida en %d' %(n,cadena,booleano+1))   
                    n += 1
                fp.close()   
            except FileNotFoundError:
                print('Fichero no encontrado o automata no disponible',file=sys.stderr)


'''Cadenas de prueba del fichero cadena.txt
bafbcdb
adaedbafedacaf
abdcefa
bafbdc
acac
c
bafbcdacacb
bafbcdeada

Resultados
Linea 1 bafbcdb: valida
Linea 2 adaedbafedacaf: valida
Linea 3 abdcefa: no valida en 4
Linea 4 bafbdc: no valida en 7
Linea 5 acac: no valida en 5
Linea 6 c: no valida en 1
Linea 7 bafbcdacacb: valida
Linea 8 bafbcdeada: no valida en 7
'''    

'''Metodo Main 
Desde este metodo se invoca al metodo tratar_entrada para realizar el analsis de la misma.
'''    
if __name__ == '__main__':
    tratar_entrada()