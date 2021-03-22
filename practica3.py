'''
@author: Diego Alejandro Toro Ramirez
'''

import urllib.request
import regex as re
import sys


'''**************************VARIABLES GLOBALES*****************************************
'''

'''diccionario global el cual posteriormente será indexado por el nombre de las enzimas de restricción.
Y que contendrá como valores, por cada enzima, una expresión regular compilada y una lista de posiciones de
corte correspondientes a la posición del carácter ˆ en las dianas de reconocimiento de la enzima.
'''
diccionario = {}

'''Cadenas con las direcciones web de Link-Bionet para el diccionario
    y parte de de la direccion web para obtener el archivo FASTA ( faltaria concatenar el gen )
'''
direcBionet ='http://rebase.neb.com/rebase/link_bionet'
direcREBASE ='http://rebase.neb.com/cgi-bin/reb_collseq.pl?seqtype=d&enzlist='


'''ER auxiliriares precompiladas'''
blancos = re.compile(r'\s+') #detectar blancos que seran eliminados
nombreCompac = re.compile(r'\s{2,}') 
nNucleotidos = re.compile(r'\s\d+\s') #detectar el nº de nucleotidos, un digito o más entre dos blancos
corte = re.compile(r'\^') #el corte de las enzimas viene dado por el simbolo ^
#nombreEnzima = re.compile(r'\p{Lu}(\p{L}+|\d+)+') #nombre de la Enzima, Una letra mayuscula, seguida de letras o digitos
#prototipo = re.compile(r'\s\(\p{Lu}(\p{L}+|\d+)+\)') # el prototipo es igual que el nombre de la enzima pero encerrado entre parentesis
#diana = re.compile(r'(\s+[ATCGRYMKSWBDHVN\^]+)$') #La diana de reconocimiento esta formada por la concatenación de varios simbolos del lenguaje descrito


'''                    Grupo 1 nombre enzima | Grupo 2 prototipo | Grupo 3 diana
'''
toda = re.compile(r'(^(?:\p{Lu}(?:\p{L}+|\d+)+))(\s\(\p{Lu}(?:\p{L}+|\d+)+\))?((?:\s+[ATCGRYMKSWBDHVN\^]+)$)')


''' COMENTARIOS SOBRE LAS RE AUXILIARES

Se va a trabajar con una RE que validase toda una linea, y de esta forma
extraer la información mediante el uso de grupos.

#Para el resto de lineas con información util
#grupo 0 toda la linea
#grupo 1 nombre
#grupo 2 prototipo
#grupo 3 diana
                                                      
                        grupo 1              grupo2                      grupo 3
toda = re.compile(r'(^(?:\p{Lu}(?:\p{L}+|\d+)+))(\s\(\p{Lu}(?:\p{L}+|\d+)+\))?((?:\s+[ATCGRYMKSWBDHVN\^]+)$)')

Se creara un match de toda la linea
mo = re.match(toda,linea)
y luego para obtener el nombre de la enzima y la diana:
nombre = mo.group(1) 
dianaL = mo.group(3)
 

Para hallar la posicion de corte primero se obtendrá
\s+[ATCGRYMKSWBDHVN\^]+ y una vez dentro de esa cadena
volver a buscar donde se encuentra la marca \^
como veremos en la generación del diccionario mas adelante
'''



'''*****************PRINCIPALES FUNCIONES DEL PROGRAMA********************
'''


'''obtenerRecursoWeb
Este método sirve para obtener un fichero de la dirección indicada como primer parametro, 
y obtener una lista con todas las lineas de dicho fichero, la cual nos sera util en posteriores metodos.
Para ello:
    1º 
    Debemos obtener la dirección web.
    La direccion url se obtendra como resultado de la concatenacion del primer y el segundo parametro, esto es asi
    ya que este método se usa para la generación del diccionario (direcBionet) y el mapa de Dianas (direcREBASE).
    Por lo que si se usase para el mapa de Dianas, se debería pasar como segundo argumento el gen el cuál se desea
    tratar. En el otro caso, se deberia pasar la cadena vacia ''.

    2ª
    A continuación con nuestra dirección url ya formada se invoca al método urlopen()
    inlcuido en el paquete estándar urllib.request el cual  que devuelve un objeto equivalente a un fichero abierto con open().
    El resultado del método es un objeto sobre el que se puede iterar para obtener las distintas líneas que lo componen.
    
    3º    
    Vamos añadiendo las distintas lineas a nuestro buffer final al mismo tiempo que las vamos "traduciendo"
    ya que hay que tener en cuenta que el paquete urllib.request devuelve cadenas binarias, ya que
    el recurso podría ser una imagen o un vídeo. Por lo que si sabemos que se trata de texto, como es el caso,
    podemos llamar al método decode() sobre las líneas para convertirlas en cadenas de caracteres
    normales sobre las cuales se puede hacer el resto del procesamiento.
'''
def obtenerRecursoWeb(direccion,opcional):
    try:
        url = direccion + opcional
        link = urllib.request.urlopen(url)
        buffer = []
        for linea in link:
            buffer.append(linea.decode().strip())
            #print(linea.decode().strip())
        return buffer
    except IOError:
        print('link_bionet no disponible',sys.stderr )


'''GenerarRE
Las cuatro primeras letras del alfabeto de la diana coinciden con las bases nitrogenadas del
ADN. Las restantes letras son un código extendido de las cadenas de ADN que permiten representar
una combinación de las bases que pueden aparecer en la posición de dicha letra.
Teniendo en cuenta el código extendido, formamos una expresión regular en donde las letras
R,Y,M,K,S,W,B,D,H,V,N se sustituyen por subexpresiones regulares que sólo emplean
A,C,G,T.

Para ello debemos hacer un analisis de casos, donde recorramos la cadena original
concatenando letras a una nueva lista según proceda. Observar que las letras del alfabeto original
no se sustituyen.
 
Para que las ER , multilinea tengan la forma adecuada, las ER simples tambien tendrán que estar entre parentesis.
Este pequeño coste no tiene impacto en las ER 'simples' y simplifica bastante el codigo.
Por lo que el primer caracter y  ultimo siempre seran ( y ) respectivamente.

Finalmente convertimos la lista creada en una cadena con el método join.

'''
def generarRE(Diana):
    l=list(Diana)
    c=[]
    c.append('(')
    for x in range(0,len(l)):
        if l[x]=='A':
            c.append('A')
        
        elif l[x]=='C':
            c.append('C')
        
        elif l[x]=='G':
            c.append('G')    
        
        elif l[x]=='T':
            c.append('T')
                    
        elif l[x]=='R':
            c.append('[A|G]')
            
        elif l[x]=='Y':
            c.append('[C|T]') 
            
        elif l[x]=='M':
            c.append('[A|C]')
            
        elif l[x]=='K':
            c.append('[G|T]')
            
        elif l[x]=='S':
            c.append('[C|G]')
            
        elif l[x]=='W':
            c.append('[A|T]')
        
        elif l[x]=='B':
            c.append('[C|G|T]')
        
        elif l[x]=='D':
            c.append('[A|G|T]')
            
        elif l[x]=='H':
            c.append('[A|C|T]')
            
        elif l[x]=='V':
            c.append('[A|C|G]')
        
        elif l[x]=='N':
            c.append('[A|C|G|T]')                           
    c.append(')')                         
    return "".join(c)
          
'''formarCadenaCompleta
Una vez hemos obtenido la lista con las cadenas asociadas a un gen mediante la llamada al metodo  obtenerRecursoWeb
debemos obtener:
    + el nº total de nucleotidos.
        Para ello hemos definido una RE, que nos servirá a obtener el número preciso.
        Dicha información se encuentra en la posición 1 de la lista, dentro de una cadena.
        Para "sacar" dicho valor de dicha cadena, nos apoyado en la funcion findAll del paquete Regrex ,
        la cual mediante una RE que hemos precompilado de forma global, encuentra todas las coincidencias y devuelve una
        lista con estas. Debido al formato de los ficheros FASTA que hemos obtenido, tenemos la garantia que en dicha 
        linea solamente se encontrara una coincidencia y el trozo de cadena con el n de nucleotidos por tanto se encontrara en la
        posicion 0 de dicha lista.
        Finalmente mostramos por pantalla el número de nucleotidos.

    + una cadena de ADN completa sin saltos de línea ni espacios en blanco.
        Es importante observar que al usar el metodo  obtenerRecursoWeb para obtener el fichero FASTA con el ADN
        de los genes, las líneas impares de la respuesta del servidor son líneas vacías. Por lo que el recorrido se hace
        mediante un bucle indexado de las posiciones impares de la lista.
        Menos el primer elemento que tiene un tratamiento especial, el resto de elementos los tratamos concatenanlos
        en una unica cadena.
        Finalmente debemos eliminar los espacios en blancos que han quedado, para ello que nos apoyamos en el metodo sub
        del paquete regrex, el cual a partir de una RE que hemos precompilado anteriormente, hara match con dicha RE (captura 
        espacios en blanco) y los eliminara de la cadena, sustituyendolos por la cadena vacia "".
        Finalemente devolvemos la cadena ya tratada.
''' 
       
def formarCadenaCompleta(cadena):
    aux=''
    for i in range(1,len(cadena),2):
        if(i == 1) :
            print('--------------' + nNucleotidos.findall(cadena[i])[0] + 'nucleótidos' ) 
        else: 
            aux += cadena[i]     
    aux = blancos.sub("",aux)
    print(aux)
    print('--------------')
    return aux



'''generarDiccionario()
Construye un diccionario indexado por el nombre de las enzimas de restricción.
Por cada enzima se debe almacena en el diccionario una expresión regular compilada y una lista de posiciones de
corte correspondientes a la posición del carácter ˆ en las dianas de reconocimiento de la
enzima. Encontraremos más detalles de como se implmenta este metodo en los comentarios del mismo
    
 
***COMENTARIOS MUY IMPORTANTES***

***DECISIONES DE IMPLEMENTACIÓN*********************************************************************************************************************

*****forma del diccionario*****
Los diccionarios de tuplas, de arrays o de conjuntos no me dejan indexar los elementos, o las insercciones son desordenadas
por ejemplo un valor {ER, posicion } y otro valor para otra clave tendria la forma { posicion, ER }
get devuelve un conjunto que no puedo indexar. No se puede hacer diccionario.get(nombre)[0]
si el diccionario fuera de la forma: diccionario[nombre] = [ER,posicion]

Este problema se ha solucionado creando un diccionario
cuyos valores son otros diccionarios.
De esta forma podemos obtener el diccionario asociado a una clave de nuestro diccionario
y obtener el mapa de claves de este segundo diccionario, el cual tendra siempre dos claves, 
por una lado (er) cuyo valor asociado es el valor de la ER propiamente dicha
por otro lado (dianas) cuyo valor asociado a esta sera una lista de posiciones (varios elementos si la ER es multilinea).


****Lista de Posiciones de Corte*******************
Debido a que el diccionario se va generando de forma secuencial mientras se lee el fichero WEB link-bionet,
para una ER asociada a una enzima, se asocia una lista con las posiciones de corte segun la ER. De esta forma
si por ejemplo la ER, tuviera varios grupos (1)|(2)|(3)  porque es multilinea, la posicion de corte del grupo 1
se corresponderia con la posicion 0 de la lista de posiciones [cortegrupo1 , cortegrupo2, cortegrupo3]
debido al tratamiento secuencial del programa esta correspondencia se puede garantizar.
Dicha correspondencia, nos sera de gran utilidad en la  generacion del mapa de dianas.


******tratamiento del fichero Recurso Web************
El metodo obtenerRecursoWeb nos devuelve una lista con las lineas de datos a tratar por lo que será más eficiente
tratar de forma especial ciertas lineas ( las 10 primeras que no contienen informacion relevante)
en vez de eliminarlas ya que supondria un desplazamiento de todos los elementos de la lista.


**OPTIMIZACIONES PLANTEADAS*********************************************************************************************************************

*****No hacer diccionario de ER precompiladas*************
Desde la pagina oficial de pyhton del paquete RE
https://docs.python.org/3.1/library/re.html
Dice:
Las versiones compiladas de los patrones más recientes pasados ​​a re.match (), re.search () o re.compile () se almacenan en caché,
por lo que los programas que usan solo unas pocas expresiones regulares 
a la vez no deben preocuparse de compilar expresiones regulares.

El diccionario va almacenaria las ER sin precompilar, como strings, y una vez se necesiten 
seran precompiladas. Ya que si lo pensamos, en pocos casos tendremos que generar el mapas de dianas 
de todas las enzimas, por lo que resulta algo mas eficiente que se vayan precompilando a medida que se
van necesitando-solicitando. 




****Optimizar el diccionario con la enzima prototipo**********
Ejemplo:
FspMSI (AvaII)                    G^GWCC
por tanto
AvaII                             G^GWCC
La idea será por tanto buscar el prototipo antes en el diccionario
El problema será que pasa si por ejemplo:
AbaDI (PvuRts1I)                  CNNNNNNNNNNN^
AbaDI (PvuRts1I)                  ^NNNNNNNNNG
AbaHI (PvuRts1I)                  CNNNNNNNNNN^

Dicho prototipo no lo he generado aún,por la forma en la cual se esta recorriendo
el fichero web link bionet.

debo buscarlo, si no esta en el mapa de Dianas:
               generar una entrada usando el prototipo y la cadena
                y despues generar otra entrada usando la enzima que estaba tratando
Esto me ocasiona el problema de que:
Cuando me trate la linea correspondiente a dicho prototipo
tratare la linea como una RE multilinea -> creando duplicados en la RE (a|b) | (a|b)
    Solución->  cuando este tratando esa linea,  mirar si el valor de la entrada
    con ese nombre , la RE, es igual que la nueva RE de la linea

Merece la pena dicha optimización? 


**************Simplificar las ER que repiten muchas letras
[E][E]  -> E{2}
-> Muy costoso recorrer las cadenas de ER
  
'''
def generarDiccionario():
    print('==============')
    print('Cargando bionet ...')
    #Obtenemos el fichero con todas las enzimas
    entrada = obtenerRecursoWeb(direcBionet,'')
    contador=0
    #Recorremos dicho fichero
    #Nos saltamos las 10 primeras lineas
    for linea in entrada:
        if(contador < 10) :
            contador=contador+1
        else:
            mo = re.match(toda,linea)
            #obtemos la diana con findall, devuelve un array con la unica diana que hay en la linea, con groups no funciona #m1 = re.match(diana,linea)
            #m1 = re.findall(diana,linea)
            
            #En el fichero pueden haber lineas vacias como la ultima
            if ( mo != None ): #and m1!=None
                nombre = mo.group(1) #obtemos el nombre de la enzima usando group
                dianaL = mo.group(3) #obtemos la diana de la linea usando group
                #print(mo.groups())
                dianaAux = blancos.sub("",dianaL) #Le quitamos los blancos de delante a la diana  #m1[0]
                #print(dianaAux)
                posicion=0 #Por defecto si no esta el caracter ^ en la cadena, la posicion de corte es 0
                po = re.search(corte,dianaAux) #Buscamos en la diana sin blancos, el caracter `^
                if(po != None ): #Si la busqueda ha sido exitosa
                    posicion = po.start() #obtenemos la posicion dentro de la diana sin blancos donde se encuentra dicho caracter
                    dianaAux = corte.sub("",dianaAux) #quitamos el caracter de la cadena
                expresionRegular = generarRE(dianaAux) #llamamos al metodo generarRE para generar la RE asociada a la diana de forma completa
                
                #Buscamos el nombre de la enzima en el diccionario:
                #si se encuentra, eso quiere decir que se trata de una enzima multilinea, y por tanto debemos crear una nueva ER
                if nombre in diccionario:
                    
                    for i in diccionario.get(nombre).keys(): #obtenemos su mapa de claves, el cual solo contiene una clave, la cadena que identifica la ER
                        if (i == 'er') :
                            aux=diccionario.get(nombre).get(i).pattern
                        elif (i=='dianas') :
                            posiciones= diccionario.get(nombre).get(i) #y con esta clave obtenemos el valor asociado a este subdiccionario, la lista de posiciones
                        #aux = i.pattern
                        #obtenemos la lista de posiciones
                        #print(aux)
                    
                    posiciones.append(posicion) #añadimos la nueva posición de esta diana   
                    #print(aux)
                    CadenaMultilinea = aux + '|' + expresionRegular #creamos una nueva cadena que represente la ER multilinea
                    ERMultilinea = re.compile(CadenaMultilinea)
                    diccionario[nombre] = { 'er': ERMultilinea, 'dianas':  posiciones } #Actualizamos la entrada de la enzima de nuestro diccionario principal 
                    #con la nueva ER multilinea y la lista de posiciones actualizada
                #En caso de que la enzima no tenga una entrada en el diccionario, sera una nueva entrada
                else :
                    listaPosiciones = [] #Creamos una lista de posiciones
                    listaPosiciones.append(posicion) #ya sea la posicion por defecto o la obtenida por el caracter de corte, la añadimos a la lista
                    ERMultilinea = re.compile(expresionRegular)
                    diccionario[nombre] = {'er': ERMultilinea, 'dianas': listaPosiciones } #insertamos la ER y la lista De posiciones de corte, la cual si la enzima no es
                    #multilinea solo tendra un elemento           
    print('Carga finalizada')
    print('--------------')


'''generarMapaDianas
Este metodo recibe dos parametros , la cadena de ADN completa y tratada
y la enzima que nos va a indicar la diana de reconocimiento para generar el mapa sobre la cadena de adn
Genera el mapa de Dianas es decir la lista de posiciones de corte de la enzima
(donde se encuentran las dianas) sobre la cadena ADN del gen especificado.
Para ello:
    
    1º Obtenemos la ER asociada a nuestra enzima , para ello obtenemos el diccionario
    asociado a nuestra clave (nombre enzima) y dentro de ese segundo diccionario
    obtenemos por un lado con la  clave (er) obtenemos la ER como tal
    y por otro lado con la clave (dianas) el valor asociado a dicha clave ( las lista con las posiciones de corte)
    
    2ºCreamos un iterador dada la ER, para buscar todos los match que encajan con nuestra RE
    en nuestra cadena de ADN. Usamos dicho iterador para ir recorriendo estos matches.
    Recordando la estructura del diccionario, para cada match podemos determinar especificanmente con que grupo de la ER
    hay coincidencia, y de esta forma obtener la posicion de corte asociada en la lista de posiciones de corte que hemos obtenido en el paso anterior.
    De esta forma, obteniendo solamente la posición inicial del match con .start(), y sumandole dicha posicion de corte asociada a dicho grupo
    podemos determinar la diana en la cadena de ADN.
    Añadimos dicha información a una lista.
    
    3º Finalmente si ha producido al menos una coincidencia, mostramos dicha información por pantalla
    para ello , transformamos la lista obtenida en una cadena y formateamos la salida de acuerdo con la especificacion del problema

'''
def generarMapaDianas(cadena,enzima):
    lista = []
    for i in diccionario.get(enzima).keys():
        if (i == 'er') :
            RE=diccionario.get(enzima).get(i)
        elif (i=='dianas') :
            posiciones= diccionario.get(enzima).get(i)
            #aux=i
            #print(i)       
    #ER = re.compile(aux)        
    iterador = re.finditer(RE, cadena)
    for sub in iterador:
        for i in range(0,len(posiciones)):
            if sub.group(i+1):
                lista.append(sub.start()+posiciones[i])                  
    
    if len(lista) != 0 :
        ListaCadena = str(lista).strip('[]')
        pantalla = enzima + ' # ' + '[' + ListaCadena + ']'
        print(pantalla)
        
  

''' control_iteracion_gen
Este método auxiliar sirve, como su nombre indica para tener un control sobre el bucle en el cuál se contruye
el mapa de dianas a partir del gen introducido por el usuario. 
Para ello:
 1º Se pide al usuario que introduzca el nombre de un gen por teclado.
 2º Si el nombre del gen es la cadena vacía, finalizará la iteración.
 3º Si no es asi, se comprueba la validez del gen:
    Para ello , se realiza una llamada al metodo obtenerRecursoWeB 
    En dicho metodo se concatenará la direccion estandar direcREBASE con el gen introducido por el
    usuario, generando (como hemos comentado anteriormente, la dirección web que se abrira).
    Si dicha dirección no existe porque el gen introducido no es correcto, 
    el servidor devolverá un fichero con la cadena "No results to print ..."
    
        Por lo que si la primera cadena de la lista devuelta por el metodo es igual a la cadena 
        que hemos mencionado anteriormente , entonces el gen no será la valido. 
        Y se le se informará al usuario.
    
        En caso contrario se asumira que es valida,  y entonces trataremos la lista obtenida del fichero FASTA
        para obtener el mapa de dianas mediante la llamada al metodo  generarMapaDianas() el cual mostraremos por pantalla...
    
    Finalmente se le pasa el control a la iteración de la enzima mediante la llamada al metodo control_iteracion_enzima  
'''
        
        
def control_iteracion_gen():
    while True:
        gen = input("Gen >>  ")
        if (gen == ''):
            print('==============')
            break
        else :
            # ¿HACER esta busqueda con un match ?
            REBASE = obtenerRecursoWeb(direcREBASE, gen)
            if ('No results to print...' == REBASE[0] ) :
                print('El Gen: ' + gen + ' no es valido'  )
                break
            else:
                control_iteracion_enzima(formarCadenaCompleta(REBASE))        


'''control_iteracion_gen
 Recibe como parametro una cadena la cual se corresponde con la cadena de ADN completa
 y preparada asociada al gen que ha introducido el usuario en el metodo de control del gen.
 Se puede decir que es como una extensión o segunda parte del metodo de control anterior, control_iteracion_gen,
 ya que solo será invocado desde este si se han cumplido las condiciones indicadas.
 En este bucle:
 1º 
     Se pide al usuario que introduzca una cadena para identificar una enzima de reconocimiento.
 2º
     Si se introduce la cadena vacía, finalizará la iteración, y por ende se volverá al control anterior,
     volviendo a la iteración de este.
 3º  
     Si la cadena introducida como enzima no es vacia:
     primero se comprobará si dicha 'clave', se encuentra en el
     diccionario;
     
     Si es asi, se generara el mapa de Dianas de dicha enzima en la cadena
     de ADN del gen.
     
     Si no se encuentra en el diccionario, entonces se asume que se trata
     de una RE, por lo que se busca en el mapa de claves del diccionario
     todas las claves que hagan match con dicha expresión.
     Si no hace match con ninguna, entonces se asume que el nombre de
     la enzima es incorrecto.
  
  4º 
      Si no se rompe el bucle introduciendo la cadena vacia entonces,
      se repite esta iteración
 
'''                                    
def control_iteracion_enzima(cadena):
    while True:
        enzima = input("Enzima >>  ")
        if (enzima == ''):
            print('--------------')
            break
        else :
            #comprobar en el mapa de claves no el diccionario entero
            if enzima in diccionario:
                generarMapaDianas(cadena,enzima)
            else:
                nombreEnzimaRE = re.compile(enzima)
                Nincorrecto = True #se hace con un booleano para 
                #evitar imprimir todas las veces que no hace match, e imprimirlo solamente una vez al final
                for i in diccionario.keys():
                    if(nombreEnzimaRE.fullmatch(i)):
                        generarMapaDianas(cadena, i)
                        Nincorrecto = False       
                if Nincorrecto :
                    print('Nombre de enzima incorrecto')
                print('--------------')        


'''PRUEBAS INPUT
'''
#C.AalSMS7ORF2591P
#FaiI               
                
                     
'''PROGRAMA
'''
'''Desde el metodo main, se invocará por un lado a la 'generación' del diccionario
y posteriormente  al control de la iteración principal.
'''       
if __name__ == '__main__':
    generarDiccionario()
    #print(diccionario)
    control_iteracion_gen()
    