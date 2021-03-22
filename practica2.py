'''
@author: Diego Alejandro Toro Ramirez
'''

from tkinter import Tk,StringVar,Frame,LabelFrame,Label,Entry,Button
from tkinter.filedialog import askopenfile,asksaveasfile
from tkinter.messagebox import showinfo,showerror
import regex as re

class Formulario(Frame):
    def __init__(self,parent=None):
        '''Crea la estructura gráfica(Frame)'''
        Frame.__init__(self,parent)
        self.pack(expand=False)
        
        '''Diccionario que almacenará los datos de los diversos clientes por clave NIF '''
        '''Los valores asociados a cada clave, son a su vez , otros diccionarios.
           De esta manera por ejemplo para la clave 29522188X
           tendriamos que UNO de sus valores asociados es el diccionario donde cuya clave 'Nombre'
           que asocia unicamente el valor 'Toro Ramirez, Alejandro'
           
            datos[ Clave1  ]= {
                    'Clave_Nombre': valor del nombre,
                    'Clave_Email':  valor del email,
                    'Clave_Teléfono': valor del telefono,
                    'Clave_Tarjeta': valor de la tarjeta,
                    'Clave_Matrícula': valor de la matricula,
                    'Clave_Fecha': valor de la fecha
                    }
        '''
        self.datos = dict() 
        '''Estructuras auxiliares que nos ayudarán a automatizar diversas funciones'''
        
        '''Estas estructuras estan rellenadas todas en el mismo orden de tal forma que por ejemplo 
        el elemento i=0 de la lista names el cual seria 'nif' tendria una correspondencia con el elemento i=0 de la lista valorCampos
        el cual seria el string (por ejemplo 29512331X) introducido en la entrada correspondiente i=0 de la lista entradaCampos'''
        ''' Lo que conseguimos con esto como ya veremos más adelante es tener una correspondencia entre los elementos de las distintas listas
        y de esta manera poder automatizar comprobaciones y llamadas en otros metodos mediante un recorrido indexado de las listas'''
        
        self.valorCampos = []
        self.entradaCampos = []
        self.names = []
        self.ERCampos = []
        
        '''RE para la compactacion'''
        self.blancos = re.compile(r'\s|\-')
        self.nombreCompac = re.compile(r'\s{2,}')
        
        '''Llamada para la comprobación dinamica de los diversos campos'''
        self.cmd = parent.register(self.actualizar)
        '''Llamada para crear el formulario(labels) asi como su diversos campos'''
        self.crear_componentes()
    
    '''ACTUALIZAR()
    El método actualizar nos va a permitir realizar una comprobación en 'tiempo real'
    para determinar si el campo que estamos escribiendo tiene el formato adecuado
    
    Para ello, 
    1º recorremos la lista que contiene los nombres de todas las entradas (esta lista es creada en el metodo crear_componentes)
    2º comprobamos que dicho elemento (el string con el nombre de la entrada) se corresponde con el campo el cual esta recibiendo 
    datos de entrada ( se esta escribiendo)
    3º Si es asi, entonces gracias a la indexacion propuesta (el paso 2º nos sirve para determinar que campo i de todas las listas se esta tratando )
    podemos determinar si el texto de entrada por el momento hace match con la ER asociada al campo que se esta tratando
    4º Si por el momento hace match el fondo de la entrada i asociada a dicho campo se pinta de blanco
       En caso contrario el campo se pinta de color rojo claro
    
    '''    
    def actualizar(self,campo,texto):
        #print(campo,texto)  para ver que cadena se esta tratando con cada pulsacion de tecla
        for i in range(len(self.names)):
            if self.names[i] in campo:
                if  self.ERCampos[i].fullmatch(texto):
                    self.entradaCampos[i].config(background='white')
                else:
                    self.entradaCampos[i].config(background='#F4838F')#color en hexadecimal  https://www.color-hex.com  se debe anteponer #
        return True
        
    '''CREAR_COMPONENTES()
    Creara los componentes graficos como etiquetas, campos y botones de la ventana.'''  
    def crear_componentes(self):

        # Título de la ventana    
        self.winfo_toplevel().title('ALF - Práctica 2')
        
        # INFORMACIÓN CLIENTE
        '''Creamos el LabelFrame que define un titulo un marco dentro de la ventana de la aplicación'''
        lframe = LabelFrame(self,text='CLIENTE')
        '''columnspan,cuantas filas pueda extenderse un componente si fuera necesario
           padx,pady para controlar los margenes '''
        lframe.grid(row=0,column=0,columnspan=3,padx=(10,10),pady=(10,10),ipadx=5)
        
        '''El marco nos servira para agrupar los 7 campos del formulario
           organizados en filas, donde en cada fila tendremos
           etiqueta campo_donde_rellenar_datos
        '''
        
        '''############CAMPOS######################
        Para cada uno de los 7 campos seguiremos el siguiente procedimiento:'''
        
        # NIF
        '''Primeramente definimos la etiqueta del campo ( dentro del marco anterior lframe)'''
        lab = Label(lframe,width=15,text='NIF (*)')
        '''Indicamos la fila y la columna de la etiqueta'''
        lab.grid(row=0,column=0)
        
        '''A continuación definimos el campo donde rellenaremos los datos propiamente dicho'''
        ''' Creamos una variable Valor, la cuál sera un objeto StringVar que facilita el acceso al texto que 
        contiene el campo, tanto para leerlo como para modificarlo'''
        self.nifV = StringVar() 
        '''Añadimos dicha variable a una lista que almacenará todo el conjunto de variables Valor
        de los otros campos con el fin de automatizar algunas funciones'''
        self.valorCampos.append(self.nifV)
        
        '''Creamos la entrada, dentro del lframe (el marco que hemos comentado antes)
        le damos un nombre, los parametros validate, validatecommand nos ayudaran en la verificación dinamica
        y por ultimo indicamos la variable Valor asociada a dicha entrada que hemos definido anteriormente'''
        self.nifE = Entry(lframe, name='nif', validate='key', validatecommand=(self.cmd,'%W','%P'), textvariable=self.nifV)
        '''Campo auxiliar con el nombre de la entrada que nos ayudara en el metodo de la verificacion dinamica'''
        self.names.append('nif')
        '''Observar que el campo esta en la misma fila que su etiqueta correspondiente'''
        self.nifE.grid(row=0,column=1)
        '''Añadimos la entrada a una lista que almacenará todo el conjunto de entradas
        de los otros campos con el fin de automatizar algunas funciones'''
        self.entradaCampos.append(self.nifE)
        
        '''Por último definimos la Expresión Regular que asociaremos a este campo
        para más adelante determinar si el texto introducido por el usuario es valido
        con respecto a las espeficaciones del campo'''
        self.nifER = re.compile(r'(X|Y|Z|\d)\d{7}-?[A-Z]')
        
        '''Añadimos la ER a una lista que almacenará todo el conjunto de todas las ER
         asociadas a los otros campos con el fin de automatizar algunas funciones'''
        self.ERCampos.append(self.nifER)
        
         
        # Nombre
        lab = Label(lframe,width=15,text='Nombre (*)')
        lab.grid(row=1,column=0)
        
        self.nombreV = StringVar()
        self.valorCampos.append(self.nombreV)
        
        self.nombreE = Entry(lframe, name='nombre', validate='key', validatecommand=(self.cmd,'%W','%P'), textvariable=self.nombreV)
        self.names.append('nombre')
        self.nombreE.grid(row=1,column=1)
        self.entradaCampos.append(self.nombreE)
        
        #Los apellidos tienen que ir a piñon fijo que ya no se permite un espacio en blanco antes de la coma pero entre los dos apellidos si, entonces no se podria usar ningun operador de repeticion
        primerApellido = r'(((\p{Lu}(\p{Ll}{2,})))((\-|((\s+[d][e])((\s+[l][a])?)\s+))(\p{Lu}(\p{Ll}{2,})))?)'
        segundoApellidocoma =r'(((\s+(\p{Lu}(\p{Ll}{2,})))((\-|((\s+[d][e])((\s+[l][a])?)\s+))(\p{Lu}(\p{Ll}{2,})))?)?)\,'
        nombre = r'\s*(((\p{Lu}(\p{Ll}{2,}))))((\s+(\p{Lu}(\p{Ll}{2,})))?)$'
        nombreRE = r''+ primerApellido +segundoApellidocoma +nombre
        #Revisar ER 
        self.nombreER = re.compile(nombreRE)
        self.ERCampos.append(self.nombreER)

        # Email (opcional) 
        lab = Label(lframe,width=15,text='Email')
        lab.grid(row=2,column=0)
        
        self.emailV = StringVar()
        self.valorCampos.append(self.emailV)
        
        self.emailE = Entry(lframe, name='email', validate='key', validatecommand=(self.cmd,'%W','%P'), textvariable=self.emailV)
        self.names.append('email')
        self.emailE.grid(row=2,column=1)
        self.entradaCampos.append(self.emailE)
        
        self.emailER = re.compile(r'(\w[\w.%+-]*@(\w[\w-]*\.)+[a-zA-Z]{2,6})?')
        self.ERCampos.append(self.emailER)
        
        
        # Teléfono
        
        lab = Label(lframe,width=15,text='Teléfono (*)')
        lab.grid(row=3,column=0)
        
        self.teléfonoV = StringVar()
        self.valorCampos.append(self.teléfonoV)
        
        self.teléfonoE = Entry(lframe, name='telefono', validate='key', validatecommand=(self.cmd,'%W','%P'), textvariable=self.teléfonoV)
        self.names.append('telefono')
        self.teléfonoE.grid(row=3,column=1)
        self.entradaCampos.append(self.teléfonoE)
        
        #problema el ultimo blanco lo deberiamos contar?
        #(\+\d{1,3}\s*)?(\d{9}|(\d{3}\s+((\d{2}\s+\d{2}\s+\d{2})|(\d{3}\s+\d{3})))) primera version
        self.teléfonoER = re.compile(r'(\+\d{1,3}\s*)?(\d{9}|(\d{3}\s+((\d{3}\s+\d{3})|(\d{2}\s+){2}\d{2})))')
        self.ERCampos.append(self.teléfonoER)
        
        # Tarjeta (opcional)
        
        lab = Label(lframe,width=15,text='Tarjeta')
        lab.grid(row=4,column=0)
        
        self.tarjetaV = StringVar()
        self.valorCampos.append(self.tarjetaV)
        
        self.tarjetaE = Entry(lframe, name='tarjeta', validate='key', validatecommand=(self.cmd,'%W','%P'),textvariable=self.tarjetaV)
        self.names.append('tarjeta')
        self.tarjetaE.grid(row=4,column=1)
        self.entradaCampos.append(self.tarjetaE)

        
        mastercard = r'((5[1-5]((\d{14})|(((\d{2}\s(\d{4}\s){2})|(\d{2}\-(\d{4}\-){2}))\d{4})))|'
        americanExpress = r'(3[47]((\d{13})|(((\d{2}\s\d{6}\s)|(\d{2}\-\d{6}\-))\d{5}))))?'
        tarjetaRE = r''+ mastercard + americanExpress
        self.tarjetaER = re.compile(tarjetaRE)
        self.ERCampos.append(self.tarjetaER)
        
        
        # Matrícula
        lab = Label(lframe,width=15,text='Matrícula (*)')
        lab.grid(row=5,column=0)
        
        self.matrículaV = StringVar()
        self.valorCampos.append(self.matrículaV)
        
        self.matrículaE = Entry(lframe, name='matricula', validate='key', validatecommand=(self.cmd,'%W','%P'),textvariable=self.matrículaV)
        self.names.append('matricula')
        self.matrículaE.grid(row=5,column=1)
        self.entradaCampos.append(self.matrículaE)
        
        #(A([BLV])?|B([AIU])?|C([ACSEORU])?|G([CEIRU])?|H([U])?|IB|J|L([EORU])?|M([ALU])?|NA|O([RU])?|P([MO])?|S([AEGHOS])?|T([EFO])?|V([AI])?|Z([A])?)\d{4}([A-Z]){0,2}
        #Matriculas nuevas ((E)\d{4}([A-Z]){3})
        
        self.matrículaER = re.compile(r'((A([BLV])?|B([AIU])?|C([ACSEORU])?|G([CEIRU])?|H([U])?|IB|J|L([EORU])?|M([ALU])?|NA|O([RU])?|P([MO])?|S([AEGHOS])?|T([EFO])?|V([AI])?|Z([A])?)\d{4}([A-Z]){0,2})|((E)\d{4}([A-Z]){3})')
        self.ERCampos.append(self.matrículaER)
        
        
        # Fecha (opcional)
        lab = Label(lframe,width=15,text='Fecha')
        lab.grid(row=6,column=0)
        
        self.fechaV = StringVar()
        self.valorCampos.append(self.fechaV)
        
        self.fechaE = Entry(lframe, name='fecha', validate='key', validatecommand=(self.cmd,'%W','%P'), textvariable=self.fechaV)
        self.names.append('fecha')
        self.fechaE.grid(row=6,column=1)
        self.entradaCampos.append(self.fechaE)
        
        #ARREGLAR ER
        combinacionDiasMeses = r'((?:(?:(?:[012]\d)|(?:3[01]))\/(?:(?:0[13578])|(?:1[02])))|(?:(?:(?:[012]\d)|(?:30))\/(?:(?:0[469])|(?:11)))|((?:[012]\d)\/(?:02)))\/'
        annos = r'((19(?:(?:7[1-9])|(?:[89]\d))|(?:20(?:(?:[0]\d)|(?:1[0-8])))))'
        fechaRE = r''+combinacionDiasMeses+annos
        self.fechaER = re.compile(fechaRE)
        self.ERCampos.append(self.fechaER)
        
        
        '''
        Define los botones graficos dentro de lframe, dichos botones estan asociados a una función 
        '''
        # BOTONES
        # Label obligatorios
        lab = Label(lframe,text='(*) Campos obligatorios')
        lab.grid(row=7,column=0,columnspan=2,sticky='W')
        
        # Botón Añadir
        bot = Button(self,text='Añadir',command=self.añadir,width=8)
        bot.grid(row=1,column=0)
        
        # Botón Modificar
        bot = Button(self,text='Modificar',command=self.modificar,width=8)
        bot.grid(row=1,column=1)
        
        # Botón Buscar
        bot = Button(self,text='Buscar',command=self.buscar,width=8)
        bot.grid(row=1,column=2)
        
        # Botón Borrar
        bot = Button(self,text='Limpiar',command=self.borrar,width=8)
        bot.grid(row=2,column=0,pady=(0,10))
 
        # Botón Cargar
        bot = Button(self,text='Cargar',command=self.cargar,width=8)
        bot.grid(row=2,column=1,pady=(0,10))
        
        # Botón Guardar
        bot = Button(self,text='Guardar',command=self.guardar,width=8)
        bot.grid(row=2,column=2,pady=(0,10))
    
    
    ''' VALIDAR
        Comprueba que todas los campos cumplen con el formato especificado
        Para ello,
        1º Recorre la lista con el valor de todos los campos 
        2º Obtiene su valor y lo asignamos a una variable auxiliar
        3º Si hace match el fondo de la entrada i asociada a dicho campo se pinta de blanco
           En caso contrario el campo se pinta de color rojo claro
        4º Se tratan todos los campos porque es interesante indicarle al usuario que campos son incorrectos
        5º Por ello una vez tratados todos, si alguno no hace match, la variable valido se le asigna el valor de False
        6º Se devulve la variable valido que indica si todos los campos son validos
        
        Comentar que el campo fecha requiere de una validacion externa a la RE para la comprobacion de si la fecha es correcta
        si el año es bisiesto.Se saca el valor de los campos mediante grupos. Estos campos son strings aunque contengan "numeros"
        asi que para poder operar con el año se debe realizar una conversion de tipos
    '''    
    def validar(self):
        valido=True
        for i in range(len(self.valorCampos)):
            aux = self.valorCampos[i].get()
            
            if  self.ERCampos[i].fullmatch(aux):
                if i == 6 :
                    mo = self.ERCampos[i].match(aux)
                    DiaMes = mo.group(1)
                    Anno=int(mo.group(3))
                    if (DiaMes == '29/02'):
                        if not((Anno % 4)==0 and ( (Anno % 100 ) !=0 or (Anno % 400)==0) ):
                            valido=False
                            self.entradaCampos[i].config(background='#F4838F')
                            showinfo('Año bisiesto', 'dia incorrecto')
                    else:
                        self.entradaCampos[i].config(background='#98FFB9')        
                #if self.ERCampos[i].fullmatch(aux):
                else:
                    self.entradaCampos[i].config(background='#98FFB9')
            else:
                self.entradaCampos[i].config(background='#F4838F')
                valido=False    
        return valido
        

    ''' COMPACTACION
    Antes de añadir los valores del formulario a nuestro diccionario
    debemos compactar por una lado
    los campos NIF, telefono y tarjeta eliminando todos los blancos o guiones
    Por otro lado el campo Nombre, sustituyendo secuencias de dos o mas blancos
    por un solo blanco
    Para ello hemos definido anteriormente dos ER las cuales hemos precompilado
    El resto de campos y pese a que el enunciado no nos indica que deben ser compactados
    los hemos compactado, pues esto no interfiere en el formato especificado, muchos
    de ellos por su ER ya imposibilitan la presencia de guiones o espacios en blanco
    y podemos automatizar el proceso a un coste bastante bajo
    Recorremos la lista con el valor de todos los campos y los compactamos quitando
    los blancos mediante la llamada sub de la expresion regular blancos, sustituyendo de esta 
    forma todos los blancos del valor del campo por la cadena vacia
    El campo correspondiente al Nombre tiene un tratamiento especial
    usando otra ER, la cual sustituye dos o más blancos por uno solo
    Finalmente añadimos el campo compactado a una nueva lista
    No lo volvemos a insertar en la lista Valores pues modificarla implicaria
    que el usuario experimentase como en la interfaz grafica los campos se compactan
    ''' 
    def compactacion(self):      
        cadenacsv = list()
        for i in range(len(self.valorCampos)):
            aux = self.valorCampos[i].get() 
            if i==1 :
                aux = self.nombreCompac.sub(" ",aux)
            else :
                aux = self.blancos.sub("",aux)
            cadenacsv.append(aux)
        return cadenacsv        
       
    '''AÑADIR
    Añade el valor de todos los campos al mapa de datos del formulario para ello:
    1º Comprobamos si todos los campos son validos
    2º Si No son validos entonces mostramos un mensaje de error indicado que la operacion no se ha completado
    En caso contrario, compactamos todos los campos, y creamos una nueva lista con los nuevos valores de los campos compactados
    3º Mediante el recorrido de dicha lista comprobamos si el nif (clave del mapa de datos) se encuentra en el mapa de datos, recordemos que por indexacion es el elemento[0] de la lista de Valores
       3ºa.Si el nif se encuentra ya registrado, devolvemos un mensaje indicando el error, pintamos dicha entrada en rojo para indicarle al usuario que dicho
       campo es incorrecto porque ese valor ya esta registrado , y borramos el valor introducido por el usuario obligandole a que vuelva a escribir dicho campo
       3ºb.Si no esta registrado, entonces lo añadimos al mapa de datos por clave nif( elemento 0) , mostramos que la operacion se ha completado exitosamente y borramos
        todos los campos del formulario para la introdución de nuevos datos.    
    '''  
    def añadir(self):
        res = self.validar()
        
        if res:
            listaAux = self.compactacion()
            if listaAux[0] in self.datos: #no comprobamos esto antes de compactar porque todos los datos en el mapa ya estan compactados
                showinfo('Añadir', 'NIF duplicado')
                self.entradaCampos[0].config(background='#F4838F')
                self.valorCampos[0].set('')
            else:
                self.datos[listaAux[0]] = {
                    'Nombre': listaAux[1],
                    'Email':  listaAux[2],
                    'Teléfono': listaAux[3],
                    'Tarjeta': listaAux[4],
                    'Matrícula': listaAux[5],
                    'Fecha': listaAux[6]
                    }
                showinfo('Añadir', 'Cliente añadido correctamente')
                self.borrar()
                print(self.datos)      
        else:
            showinfo('Añadir', 'Cliente incorrecto, modifique los campos en rojo')
        pass
    
    '''MODIFICAR
        Modifica un valor de Diccionario dada una clave(nif): para ello
        Al igual que en añadir: 
        1º Comprobamos si todos los campos son validos
        2º Si No son validos entonces mostramos un mensaje de error indicado que la operacion no se ha completado
        En caso contrario, compactamos todos los campos, y creamos una nueva lista con los nuevos valores de los campos compactados
        3º Mediante el recorrido de dicha lista comprobamos si el nif (clave del mapa de datos) se encuentra en el mapa de datos, recordemos que por indexacion es el elemento[0] de la lista de Valores
       
       En este caso, a diferencia del metodo añadir:
        
       3ºa.Si el nif se encuentra ya registrado, accedemos a esa entrada del diccionario y REEMPLAZAMOS el conjunto de sus valores 
       por los nuevos valores obtenidos en el formulario mostramos que la operacion se ha completado exitosamente y borramos
        todos los campos del formulario para la introdución de nuevos datos
       3ºb.Si no esta registrado
        devolvemos un mensaje indicando el error, pintamos dicha entrada en rojo para indicarle al usuario que dicho
       campo es incorrecto porque ese valor NO esta registrado , y borramos el valor introducido por el usuario obligandole a que vuelva a escribir dicho campo
    Importante 
    Para modificar una entrada (dni) obligatoriamente se tienen que introducir los campos obligatorios
    '''    
    def modificar(self):
        res = self.validar()

        if res:
            listaAux = self.compactacion()
            if listaAux[0] in self.datos:
                self.datos[listaAux[0]] = {
                    'Nombre': listaAux[1],
                    'Email':  listaAux[2],
                    'Teléfono': listaAux[3],
                    'Tarjeta': listaAux[4],
                    'Matrícula': listaAux[5],
                    'Fecha': listaAux[6]
                    }
                showinfo('Modificar', 'Cliente añadido correctamente')
                self.borrar()
                print(self.datos)  
            else:
                showerror('Modificar', 'sólo se puede realizar la modificación de un cliente añadido previamente')
                self.entradaCampos[0].config(background='#F4838F')
                self.valorCampos[0].set('')
        else:
            showinfo('Añadir', 'Cliente incorrecto, modifique los campos en rojo')           
        pass
        
    
    '''BUSCAR 
        Busca en el Diccionario los valores asociados a la clave dada(nif) y los establece en el formulario solo si dicha entrada existe
        Si no existe el nif, se muestra un mensaje de error y se pinta la entrada del nif de rojo para indicarle al usuario que debe modificarlo
    '''
    def buscar(self):
        nif = self.nifV.get()
        if nif in self.datos:
            datos = self.datos[nif]
            self.nombreV.set(datos['Nombre'])
            self.emailV.set(datos['Email'])
            self.teléfonoV.set(datos['Teléfono'])
            self.tarjetaV.set(datos['Tarjeta'])
            self.matrículaV.set(datos['Matrícula'])
            self.fechaV.set(datos['Fecha'])
        else:
            showerror('Buscar', 'NIF %s no existe' %nif)
            self.entradaCampos[0].config(background='#F4838F')
            self.valorCampos[0].set('')
    
    '''BORRAR Borra la información del formulario, podra ser invocada explicitamente mediante un boton
        Recorre la lista de valores de los campos del formulario y los establece a la cadena vacia, y pinta de blanco 
        todas las entradas del formulario.
    '''
    def borrar(self):
        for i in range(len(self.valorCampos)):
            self.valorCampos[i].set('')
            self.entradaCampos[i].config(background='white')
        pass
    
    '''CARGAR Carga un fichero valido con el formato csv y lo añade al diccionario, además muestra el diccionario actualizado
        tras añadir el contenido de dicho fichero. Muy importante que el fichero sea valido conforme las 
        Para ello, "abrimos el fichero."
                                        ******ANEXO******
        Función askopenfile
        El primer argumento indica el directorio inicial a partir del cual se muestran los archivos y
        carpetas. Si se indica ’.’, se especifica que se use el directorio del módulo que se está ejecutando.
        El segundo argumento es el título del cuadro de diálogo. El tercer argumento permite especificar las
        extensiones de los archivos que se tratarán como archivos seleccionables. Se especifica mediante
        una lista de tuplas, cada una de las cuales contiene una cadena para representar a cada tipo de
        archivo y una expresión regular para la extensión
                                        ******************
        Si esta abierto y tiene el formato indicado,
        leemos la primera linea del fichero, pues solo contiene el nombre de los campos 
        (***Importante*** si el fichero que se carga no tiene esta primera linea, y en su lugar tiene una linea con los datos de un usuario validos, 
        dicha linea no será tratada . Por otro lado si el fichero no tiene alguno de los campos, o el formato delimitador de los campos es incorrecto
        el programa fallará. Dado que en el ejercicio no se especifica dicha corrección de errores, se asume que como precondición los ficheros tratados
        serán correctos en los puntos comentados anteriormente)
        A continuación, para cada linea del contenido del fichero, 
            1º Por un lado creamos una "lista de valores" auxiliar que nos servirá para
               almacenar todos los campos de UNA linea una vez tratada.
               
               Por otro lado separamos los campos, mediante el delimitador ","
               Y almacenamos los campos en una lista campos.
               
            2º Recorremos dicha lista de campos eliminando para cada uno de los
                campos los delimitadores '"' del principio y del final
                
            3º Añadimos el campo ya tratado a la lista de lista de valores previamente definida
            
            4º Ahora ya podemos, introducir en nuestro diccionario los valores de la linea tratada,
            usando como clave el primer campo ( el primer elemento de la lista de valores , es decir el nif)
            y como valores tenemos el resto de elementos de la lista de valores, los cuales asociamos de acuerdo a la estructura
            del diccionario comentada en puntos anteriores.
    '''    
    def cargar(self):
        fichero = askopenfile(initialdir = '.',title = 'Abrir',filetypes = [('CSV','*.csv')])
        if fichero:
            fichero.readline()
            for linea in fichero:
                linea = linea.strip()
                campos = linea.split('","') # OJO REVISAR QUE NO CORTE EL CAMPO NOMBRE CON ,
                valores = list()
                for campo in campos:
                    campo = campo.strip('"')
                    valores.append(campo)
                if valores[0] in self.datos: 
                    showinfo('Cargar', 'Advertencia, NIF Cargado existente en el mapa, Sobreescritura de campos')   
                self.datos[valores[0]] = {
                    'Nombre': valores[1],
                    'Email':  valores[2],
                    'Teléfono': valores[3],
                    'Tarjeta': valores[4],
                    'Matrícula': valores[5],
                    'Fecha': valores[6]
                    }
            print(self.datos) 
            showinfo('Cargar', 'Fichero cargado correctamente')
            fichero.close()


    
    '''GUARDAR Guardamos los datos del diccionaro en un fichero csv, para ello:
        1º Creamos un buffer donde introducimos la primera linea  del futuro fichero la cual contiene los nombres de los campos
        2º Recorremos el mapa mediante sus claves
        3º Con cada clave:
            Creamos una cadena donde concatenamos los delimitadores de comillas '"' la clave '"' ','
            Ahora, para concatenar el resto de valores asociados a dicha clave, debemos recordar como esta construido el diccionario:
            datos[ Clave1  ]= {
                    'Clave_Nombre': valor del nombre,
                    'Clave_Email':  valor del email,
                    'Clave_Teléfono': valor del telefono,
                    'Clave_Tarjeta': valor de la tarjeta,
                    'Clave_Matrícula': valor de la matricula,
                    'Clave_Fecha': valor de la fecha }
            Vemos que el valor asociados a una clave, son otros 'diccionarios',
     
        4º Obtenemos el valor asociado de la clave, y recorremos todos los diccionarios, donde cada
        cada diccionario  se representa por su 'clave'. Finalmente para obtener el valor de ese campo
        debemos obtener en ese diccionario, el valor asociado a esa clave. 
        De esta forma  por ejemplo, para la clave 29522188A, el valor asociado seria el conjunto de diccionarios
        {
       'Clave_Nombre': valor del nombre,
       'Clave_Email':  valor del email,
       'Clave_Teléfono': valor del telefono,
       'Clave_Tarjeta': valor de la tarjeta,
       'Clave_Matrícula': valor de la matricula,
       'Clave_Fecha': valor de la fecha
        }
        Recorremos este conjunto, por claves, por lo que en el primer diccionario ['Clave_Nombre': valor del nombre]
        para la clave 'Clave_Nombre', el valor seria 'valor del nombre'
        
        5º Concatenamos el valor de cada campo a la cadena que habiamos definido anteriormente, de tal forma que cuando se recorra el conjunto de diccionarios
        asociados a la clave por ejemplo 29522188A , ya tendremos la linea completa con los datos asociados a dicho usuario.
        
        6ºAñadimos dicha linea a la lista de lineas que hemos definido para que haga la funcion de buffer.
        7ºFinalmente una vez recorrido todo el diccionario , volcamos el contenido del buffer al fichero                  
    '''
    def guardar(self):
        fichero = asksaveasfile(initialdir = '.',title = 'Guardar',filetypes = [('CSV','*.csv')])
        if fichero:
            #recorrer el mapa por claves
            lineas=[]
            lineas=['"NIF","NOMBRE","Email","Telefono","Tarjeta","Matricula","Fecha"\n']
            for i in self.datos.keys():
                valores= self.datos.get(i)
                cadena='"'+i+'"'
                for j in valores:
                    campo=valores.get(j)
                    cadena+=','+'"'+campo+'"'
                cadena=cadena+'\n'
                print(cadena)    
                lineas+=cadena
                
            fichero.writelines(lineas)
            showinfo('Guardar', 'Fichero añadido correctamente')
            fichero.close()
            
        else:
            showerror('Guardar', 'Fichero no existe - no es valido')
            #fichero.close()

    
    ''' Coleccion de datos de entrada
    29522188V
    X3455782X
    12312312X
    Z1234567X
    
    Toro-Bravo Ramirez de la Fuente,Diego Alejandro
    Smith, John
    Pérez Sánchez, Ana
    Nicolás de Quevedo Robles, Juan
    Marín Hernández-Pérez, José Manuel

    diegotororamirez@um.com
    
    818215423
    918 215 423
    666 215 423
    568 21 54 23
    +34968212565
    +1 268212565
    +12 668 212 565
    
    +1 268212565
    5521-1234-1234-1234
    5123123412341234
    5123 1234 1234 1234
    5521-1234-1234-1234
    342112345612345
    3421 123456 12345
    3721-123456-12345
    
    A3564AB
    CC2342B
    MA5332
    CC2342B
    
    31/08/2018
    31/07/1971
    29/02/1980
    30/04/2000
    '''
                  
if __name__ == '__main__':
    '''Constructor de la ventana principal de la aplicación'''
    master = Tk()
    '''Se invoca al constructor del formulario(contenido de la ventana anterior)'''
    f = Formulario(master)
    '''Gestión de  eventos gráficos de la aplicación'''
    master.mainloop()
    