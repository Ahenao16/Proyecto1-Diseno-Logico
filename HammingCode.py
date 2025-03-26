#ITCR-Proyecto 01- Diseño Lógico - Docente: Carlos Jiménez Robles- Estudiantes: Alejandro Henao, Cristian Rosa, Mariano Mora 

#Se importan los paquetes necesarios para la creación de la interfaz gráfica del programa (Tkinkter y Matplotlib)
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class Interfaz: #Se crea una clase (basada en POO) para la interfaz del programa 
    def __init__(self, Ventana): #Se define el método __init__ como constructor  de una instancia u objeto de la clase llamado "Ventana" que corresponde a la ventana principal
        #Se definen las propiedades o atributos de la clase "Ventana":
        self.Diccionario_valido = ("0","1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f") #Simbolos válidos para ingresar el dato hexadecimal
        self.Diccionario_valido_error = ("0","1", "2", "3", "4", "5", "6", "7", "8", "9") #Símbolos inválidos
        self.Ventana = Ventana #La instancia de la clase "Ventana" tambien se llama Ventana
        self.Ventana.title("Código Hamming") #Titulo, tamaño, posibilidad de ajustar su tamaño y un color de fondo 
        self.Ventana.geometry("1200x600")
        self.Ventana.resizable(False, False)
        self.Ventana.configure(bg="#E9E0D6")
        self.numero_final = "" #Se inicializan vacios los espacios para representar los números convertidos a las distintas bases (Hexadecimal,octal, binario y decimal)
        self.numero_binario = ""
        self.numero_octal = ""
        self.numero_decimal = ""
        self.cantidad_BitsParidad = 0 #Inicialmente se cuentan con cero bits de paridad para el dato registrado en hexadecimal
        self.matriz_paridad = [] #Se inicializa vacía una matriz que contiene los bits de paridad
        self.numero_con_paridad = "" #Se dejan libres los espacios para representar los números con paridad, error, el bit de error, etc. 
        self.placeholder_numero_con_paridad = ""
        self.numero_con_error ="" 
        self.estado_paridad = ""

  
        self.canvas = tk.Canvas(self.Ventana, bg="#E9E0D6") #Se crea un canvas de Tkinker, ligado a una instancia de la clase Ventana
        self.canvas.pack(side="left", fill="both", expand=True) #Se configura el canvas para abarcar el espacio de la ventana 
        
        self.scrollbar = tk.Scrollbar(self.Ventana, orient="vertical", command=self.canvas.yview) #Se da la opción de la barra lateral de desplazamiento para la ventana
        self.scrollbar.pack(side="right", fill="y")
        
    
        self.canvas.config(yscrollcommand=self.scrollbar.set) #La barra es una instancia de la clase Scrollbar configurada debidamente 

  
        self.frame = tk.Frame(self.canvas, bg="#E9E0D6") #Se inicializa una instancia de Frame o Marco de Tkinter 
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw") #Permite organizar los contenidos de la ventana en posiciones fijas 

      
        self.frame.bind("<Configure>", self.on_frame_configure) 

   
        self.label_instrucciones = tk.Label(self.frame, text="Ingrese el número en hexadecimal y presione el botón. Este debe estar formado por 3 caracteres válidos (En el caso de ser un número de dos o un dígito complete el faltante con ceros). Los caracteres numéricos deben ser colocados en minúscula", font=("Arial", 12), fg="Black", anchor="center", wraplength=700, bg="#E9E0D6")
        self.label_instrucciones.pack(pady=10, padx=225) #Se crea un label o etiqueta con instrucciones para el usuario

        self.entry_numero = tk.Entry(self.frame, font=("Arial", 12)) #Inicializa el espacio para que el usuario ingrese el dato en hexadecimal
        self.entry_numero.pack(pady=10, padx=225)

<<<<<<< HEAD
        self.Boton_conversion = tk.Button(self.frame, text="Confirmar", command=self.Comprobacion_numero ,highlightthickness=2,bd=2, bg="white")
        self.Boton_conversion.pack(pady=10, padx=225) #El botón Confirmar registra el número Hexadecimal del usuario 
=======
        self.Boton_conversion = tk.Button(self.frame, text="Convertir", command=self.Comprobacion_numero ,highlightthickness=2,bd=2, bg="white",font=("Arial", 12))
        self.Boton_conversion.pack(pady=10, padx=225)
        
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768

        self.label_error = tk.Label(self.frame, text="", font=("Arial", 12), fg="#F25757", bg="#E9E0D6")
        self.label_error.pack(pady=10, padx=225) 
        
        #Se crea la tabla que despliega el resultado de la conversión de la entrada hexadecimal a base 2,8 y 10 
        self.tabla_numeros = ttk.Treeview(self.frame, columns=('Binario', 'Octal', 'Decimal'), show="headings", height=1, selectmode="none")
        self.tabla_numeros.heading('Binario', text='Binario (12 bits)')
        self.tabla_numeros.heading('Octal', text='Octal')
        self.tabla_numeros.heading('Decimal', text='Decimal')
        self.tabla_numeros.column('Binario', anchor='center', width=200)
        self.tabla_numeros.column('Octal', width=200, anchor='center')
        self.tabla_numeros.column('Decimal', width=200, anchor='center')
        self.tabla_numeros.pack(pady=10, padx=225)
        self.tabla_numeros.bind('<Button-1>', lambda event: self.handler(event, self.tabla_numeros))
        self.tabla_numeros.bind('<Motion>', lambda event: self.handler(event, self.tabla_numeros))

        self.formato_tabla_numeros = ttk.Style() #Para la tabla, se utiliza el estilo treeview, especialmente util en esta clase de aplicaciones
        self.formato_tabla_numeros.configure("Treeview", font=("Arial", 12), background="#dcdcdc", rowheight=25)
        self.formato_tabla_numeros.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        
        self.frame_NRZI = tk.Frame(self.frame) #Crea un marco vacío para la representación de NRZI
        self.frame_NRZI.pack(pady=5, padx=225)

        self.label_eleccion_paridad = tk.Label(self.frame, text="", font=("Arial", 12), bg="#E9E0D6")
        self.label_eleccion_paridad.pack(pady=5, padx=225) #Crea una etiqueta para presentar la elección al usuario del tipo de paridad 

        self.boton_paridad_par= tk.Button(self.frame, text="", font=("Arial", 12), bg="#E9E0D6",bd=0, highlightthickness=0,command=lambda:self.Llamada_paridad_par())
        self.boton_paridad_par.pack(pady=5) #Boton para la paridad par 

        self.boton_paridad_impar= tk.Button(self.frame, text="", font=("Arial", 12), bg="#E9E0D6",bd=0, highlightthickness=0,command=lambda:self.Llamada_paridad_impar())
        self.boton_paridad_impar.pack(pady=5) #Boton para la paridad impar 

<<<<<<< HEAD
    def handler(self, event,treeview): #Crea un manejador para evitar que el usuario intente modificar las dimensiones de las tablas
=======
        self.canvas_tabla= tk.Canvas(self.frame,width=400, height=300)

    def handler(self, event,treeview):
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768
            if treeview.identify_region(event.x, event.y) == "separator":
                return "break"

    def crear_tabla_paridad(self, parent, columnas): #Metodo para crear la tablar de paridad 
        for widget in self.frame.winfo_children():
<<<<<<< HEAD
            if isinstance(widget, ttk.Treeview) and widget != self.tabla_numeros:
                widget.destroy() #Elimina cualquier instancia de widget que sea un treeview pero que no sea parte de tabla_numeros 
=======
            try:
                if isinstance(widget, ttk.Treeview) and widget != self.tabla_numeros and widget != self.tabla_error:
                    widget.destroy()
            except:
                if isinstance(widget, ttk.Treeview) and widget != self.tabla_numeros:
                    widget.destroy()
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768

        tree = ttk.Treeview(parent, show="headings",height=int(self.cantidad_BitsParidad)+2) #Se hace la tabla (el arbol de treeview)
        columnas_lista = [""] #Con n cantidad de columnas
        contador_bit_datos = 1 #Se empieza con el dato 1 
        contador_bit_paridad = 1 #Igual con los bits de paridad
        fila_datos_sp = ["Datos (sin paridad)"] #Se crean dos matrices separadas para contener los datos con y sin paridad 
        fila_datos_cp = ["Datos (con paridad)"]

        for i in range(1, columnas + 1): #Para crear las columnas, las posiciones potencia de 2 (0,1,2,4,etc) se asignan a los bits de paridad
            if (2**(i - 1)) % i == 0:
                columnas_lista.append(f"p{contador_bit_paridad}")
                contador_bit_paridad += 1
            else:
                columnas_lista.append(f"d{contador_bit_datos}") #Las demás posiciones corresponden a bits de datos 
                contador_bit_datos += 1
        contador_bit_datos = 1
        contador_bit_paridad = 1
        tree["columns"] = columnas_lista #Los nombres de las columnas corresponden los bits de paridad y datos asignados previamente 

      
        for col in columnas_lista: #Por cada columna en la lista de columnas,el nombre de columna corresponde a "p_contador_bit_paridad" o "d_contador_bit_datos"
            tree.heading(col, text=col)
            if col == "":
                tree.column(col, width=150, anchor="center")
            else:
                tree.column(col, width=40, anchor="center")

        
        style = ttk.Style() #Se configura el treeview o tabla 
        style.configure("Treeview", rowheight=25)  
        
       
        for i in range(1, columnas + 1): #Si la posición es bit de paridad, coloca un espacio vacío
            if (2**(i - 1)) % i == 0:
                fila_datos_sp.append("")  
            else:
                bit_posicion = self.numero_con_paridad[i - 1] #Si es bit de dato, coloca el bit que le corresponde extrayendolo de numero_con_paridad
                fila_datos_sp.append(bit_posicion)

        tree.insert("", "end", values=fila_datos_sp)

        
        for i in range(1, self.cantidad_BitsParidad + 1): #Hace un recorrido por los bits de paridad 
            posiciones_paridad = getattr(self, f"Posiciones_p{i}") #Para cada bit de paridad, obtiene su valor y posición
            bit_paridad = getattr(self, f"p{i}")
            fila_paridad = [f"p{i}"]

            for col in range(1, columnas + 1): #Crea las filas de paridad, donde si es posición de paridad se asigna su dato correspondiente, 
            #y si es la posición de bit de paridad, agregra el valor de dicho bit de paridad 
                if col - 1 in posiciones_paridad:
                    fila_paridad.append(self.numero_con_paridad[col - 1])
                elif (2**(i - 1)) == col:
                    fila_paridad.append(str(bit_paridad))
                else:
                    fila_paridad.append("")

            tree.insert("", "end", values=fila_paridad) #Inserta lo anterior en el treeview para ir creando la tabla 

      
        for i in range(1, columnas + 1): #Construye el número de 12 bits completo, incliuyendo bits de datos y bits de paridad 
            fila_datos_cp.append(self.numero_con_paridad[i - 1])  
        tree.insert("", "end", values=fila_datos_cp)

        
        tree.pack() #Crea la tabla de paridad como un tree 
        self.tabla_paridad = tree
        tree.bind('<Button-1>', lambda event: self.handler(event, tree))
        tree.bind('<Motion>', lambda event: self.handler(event, tree))
        self.Crear_interfaz_error()
        return tree
    
    def crear_tabla_error(self, parent, columnas): #Método para generar la tabla que muestra el error según el algoritmo de Hamming 
        print("el numero con error es" + str(self.numero_con_error)) #Despliega el numero con error
        
        self.Mostrar_posiciones() #Las posiciones de paridad que se muestran dependen de la elección del usuario de hacer paridad par o impar 
        if self.estado_paridad == "par":
            self.Paridad_par_error(self.numero_con_error)
            self.Mostrar_bits_paridad()
        else:
            self.Paridad_impar_error(self.numero_con_error)
            self.Mostrar_bits_paridad()
<<<<<<< HEAD
        print(self.numero_con_error) #Se despliega el valor que presenta el error 
=======
        print("numero de testeo" + self.numero_con_error)
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768
        numero_error = self.numero_con_error
        self.Mostrar_posiciones() 
        
        for widget in self.frame.winfo_children(): #Cualquier widget ajeno a la tabla original de numeros o a la de paridad es eliminado 
            if isinstance(widget, ttk.Treeview) and widget != self.tabla_numeros and widget != self.tabla_paridad:
                widget.destroy()

        tabla_error = ttk.Treeview(parent, show="headings", height=int(self.cantidad_BitsParidad) + 1) #Se construye la tabla de error 
        columnas_lista = [""]
        contador_bit_datos = 1
        contador_bit_paridad = 1
        fila_datos_sp = ["Datos"]

        
        for i in range(1, columnas + 1): #Se llena de manera similar a la tabla original de números 
            if (2**(i - 1)) % i == 0:
                columnas_lista.append(f"p{contador_bit_paridad}")
                contador_bit_paridad += 1
            else:
                columnas_lista.append(f"d{contador_bit_datos}")
                contador_bit_datos += 1

        
<<<<<<< HEAD
        columnas_lista.append("Bit de paridad") #Se agrega una columna adicional para mostrar el valor del bit de paridad
        columnas_lista.append("Prueba de paridad") #Se muestra si la prueba de paridad para los bits de paridad resultado en un estado correcto o en error detectado
        tabla_error["columns"] = columnas_lista

        
        for col in columnas_lista: #Agrega los titulos a las nuevas columnas de la tabla de error 
            if col in ["Bit de paridad", "Prueba de paridad"]:
=======
        columnas_lista.append("Posición de error")
        columnas_lista.append("Prueba de paridad")
        tabla_error["columns"] = columnas_lista

        
        for col in columnas_lista:
            if col in ["Posición de error", "Prueba de paridad", ""]:
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768
                tabla_error.column(col, width=150, anchor="center")  
            else:
                tabla_error.column(col, width=40, anchor="center")  

            tabla_error.heading(col, text=col)

       
        style = ttk.Style() #Se configura la tabla 
        style.configure("Treeview", rowheight=25)  

     
        for i in range(1, columnas + 1): #Se llena según el número de posición, si corresponde a bit de dato o a bit de paridad 
            if (2**(i - 1)) % i == 0:
                fila_datos_sp.append("")  
            else:
                bit_posicion = numero_error[i - 1]
                fila_datos_sp.append(bit_posicion)

       
        fila_datos_sp.append("")  
        fila_datos_sp.append("")  

        tabla_error.insert("", "end", values=fila_datos_sp) #Se inserta a la tabla de error 

        # Insertar filas de bits de paridad
        for i in range(1, self.cantidad_BitsParidad + 1):
            posiciones_paridad = getattr(self, f"Posiciones_p{i}")
            bit_paridad = getattr(self, f"p{i}")
            fila_paridad = [f"p{i}"]

            for col in range(1, columnas + 1):
                if col - 1 in posiciones_paridad:
                    fila_paridad.append(numero_error[col - 1])
                elif (2**(i - 1)) == col:
                    fila_paridad.append(str(bit_paridad))
                else:
                    fila_paridad.append("")

            # Agregar bit de paridad y su estado
            fila_paridad.append(str(bit_paridad))
            fila_paridad.append("Correcto" if bit_paridad == 0 else "Error")

            tabla_error.insert("", "end", values=fila_paridad)

        tabla_error.pack() 
        self.tabla_error = tabla_error
        tabla_error.bind('<Button-1>', lambda event: self.handler(event, tabla_error))
        tabla_error.bind('<Motion>', lambda event: self.handler(event, tabla_error))
        self.label_reintentar = tk.Label(self.frame, text="Si desea ingresar otra posición a modificar presione el siguiente boton:", font=("Arial", 12), bg="#E9E0D6")
        self.label_reintentar.pack(pady=5, padx=225)

        self.boton_reintentar = tk.Button(self.frame, text="Colocar otro número", command=lambda:self.Reiniciar() ,highlightthickness=2,bd=2, bg="white", font=("Arial", 12))
        self.boton_reintentar.pack(pady=5,padx=225)
        return tabla_error

    def Reiniciar(self):
        self.boton_error.config(state="active") 
        self.boton_reintentar.destroy()
        self.label_mostrar_error.destroy()
        self.label_reintentar.destroy()
        self.tabla_error.destroy()
        self.reset_paridad()
        self.entry_posicion_error.delete(0, tk.END)
        print("Numero con error"+self.numero_con_error)
        self.Paridad_par(self.placeholder_numero_con_paridad)

<<<<<<< HEAD
    def Crear_interfaz_error(self): #Metodo para crear la interfaz que permite modificar un bit para simular un error 
=======
        
       
    def Crear_interfaz_error(self):
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768
        if hasattr(self, 'label_numero_error') and hasattr(self, 'entry_posicion_error') and hasattr(self, 'boton_error'):
            self.label_numero_error.destroy()
            self.entry_posicion_error.destroy()
            self.boton_error.destroy()
        
<<<<<<< HEAD
        self.label_numero_error = tk.Label(self.frame, text="Escriba una posición en el bit de datos a modificar de 1 a " + str(len(self.numero_binario)) , font=("Arial", 12), bg="#E9E0D6")
        self.label_numero_error.pack(pady=5, padx=225) #Etiqueta indica al usuario que debe seleccionar una posicion para alterar 
=======
        self.label_numero_error = tk.Label(self.frame, text="Escriba la posición en el bit de datos a modificar de 1 a " + str(len(self.numero_binario)) , font=("Arial", 12), bg="#E9E0D6")
        self.label_numero_error.pack(pady=5, padx=225)
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768

        self.entry_posicion_error = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_posicion_error.pack(pady=10, padx=225) #Crea el espacio para indicar el bit de datos a cambiar 

<<<<<<< HEAD
        self.boton_error = tk.Button(self.frame, text="Confirmar", command=lambda:self.Obtener_numero_error() ,highlightthickness=2,bd=2, bg="white")
        self.boton_error.pack(pady=5,padx=225) #Crea el botón de confirmación y extrae el dato del bit que el usuario deseea modificar 
=======
        self.boton_error = tk.Button(self.frame, text="Modificar", command=lambda:self.Obtener_numero_error() ,highlightthickness=2,bd=2, bg="white", font=("Arial", 12))
        self.boton_error.pack(pady=5,padx=225)
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768

    def Obtener_numero_error(self): #Metodo para obtener el número de posición donde se quiere el error 
        if hasattr(self, 'label_mostrar_error'):
            self.label_mostrar_error.destroy()

<<<<<<< HEAD
        self.numero_con_error="" #Se inicializa vacio 
        
        posicion = self.entry_posicion_error.get() #Se obtiene su posicion
=======
        self.numero_con_error=""
        posicion = self.entry_posicion_error.get()
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768
        self.label_mostrar_error = tk.Label(self.frame, text="", font=("Arial", 12), bg="#E9E0D6")
        self.label_mostrar_error.pack(pady=5, padx=225) #Se muestra con una etiqueta en la ventana del programa

        if not posicion.isdigit() or int(posicion) <= 0 or int(posicion) > len(self.numero_binario):
            self.label_mostrar_error.config(text="Posición no válida, Intente de nuevo", fg="#F25757")
            return #Si la posicion no es un digito, menor a 1, o menor a la longitud del numero en binario, se despliege un mensaje de error para el usuario

        posicion_python = int(posicion) - 1  #Las posiciones binarias comienzan en 0, las del usuario en 1, se corrige esta distincion
        lista_numero_mostrable = list(self.numero_binario)

        if lista_numero_mostrable[posicion_python] == '1': #Simula el error, cambiando un 1 por 0 y viceversa en una posicion dada
            lista_numero_mostrable[posicion_python] = '0'
        elif lista_numero_mostrable[posicion_python] == '0':
            lista_numero_mostrable[posicion_python] = '1'
        self.numero_con_error = ''.join(lista_numero_mostrable)
        self.label_mostrar_error.config(text="El número original con error es: " + self.numero_con_error, fg="#4EA699")
        
<<<<<<< HEAD
        print("El numero binario original con error es:" +str(self.numero_con_error)) #Imprime el numero binario con error en la terminal

        self.Crear_numero_error(self.numero_con_error) 
        print("El numero con error y ps es:" +str(self.numero_con_error))

=======
        self.Crear_numero_error(self.numero_con_error)
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768
        lista_numero_con_error = list(self.numero_con_error)
        paridad_index = 1  

        for i in range(len(lista_numero_con_error)): #Reconstruye los bits de paridad del numero con error 
                if lista_numero_con_error[i] == 'p':
                    bit_paridad_attr = f"p{paridad_index}"  
                    if hasattr(self, bit_paridad_attr):
                        lista_numero_con_error[i] = str(getattr(self, bit_paridad_attr))
                        paridad_index += 1  

        self.numero_con_error = ''.join(lista_numero_con_error)

<<<<<<< HEAD
        self.crear_tabla_error(self.frame, columnas=len(self.numero_con_error)) #Las columnas de la tabla de error son iguales a la longitud del numeor con error
=======
        self.boton_error.config(state="disabled")  

        print("El numero de error a probar es" + self.numero_con_error )
        self.crear_tabla_error(self.frame, columnas=len(self.numero_con_error))
>>>>>>> 7a9613c757ecd5800417a192c2140f4568b2b768
     

    def Llamada_paridad_par(self): #Funciones de llamada para crear la tabla de paridad 
        self.Paridad_par(self.placeholder_numero_con_paridad) #Con paridad par 
        self.Mostrar_bits_paridad()
        self.crear_tabla_paridad(self.frame, columnas=len(self.placeholder_numero_con_paridad))

    def Llamada_paridad_impar(self):
        self.Paridad_impar(self.placeholder_numero_con_paridad) #Con paridad impar 
        self.Mostrar_bits_paridad()
        self.crear_tabla_paridad(self.frame, columnas=len(self.placeholder_numero_con_paridad))


    def on_frame_configure(self, event=None): #Se configura el canvas 
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def Comprobacion_numero(self): #Funcion para comprobar si la entrada en hexadecimal del usurio es valida
        diccionario = self.Diccionario_valido
        numero_comprobacion = self.entry_numero.get()

        if len(numero_comprobacion) != 3: #Debe tener una longitud maxima de 3 bits
            self.label_error.config(text="El número debe tener exactamente 3 caracteres. Intente de nuevo.", fg= "#F25757")
            return

        for i in numero_comprobacion: #Debe estar formado por los simbolos permitidos en hexadecimal (0 a F)
            if i not in diccionario:
                self.label_error.config(text="El número debe estar formado por caracteres válidos. Intente de nuevo", fg= "#F25757")
                return

        self.Obtener_numero() #Se crean multiples atributos
        self.Conversor(self.numero_final)
        self.NRZI(self.numero_binario)
        self.Calculo_bits_paridad(self.numero_binario)
        self.crear_matriz_binaria(self.cantidad_BitsParidad)
        self.Posiciones_paridad(self.matriz_paridad)
        self.Mostrar_posiciones()
        self.Crear_numero_paridad(self.numero_binario)

        
    
    def Obtener_numero(self): #Mensaje que le dice al usuario cual numero ingreso 
        self.numero_final = self.entry_numero.get()
        self.label_error.config(text="Usted ingresó el número hexadecimal: " + self.numero_final, fg="#4EA699")
        return self.numero_final

    def Conversor(self,num): #Metodo para convertir el numero a las distintas bases 
        for item in self.tabla_numeros.get_children():  # Esto es para eliminar la tabla al darle 2 veces al boton
            self.tabla_numeros.delete(item)

        self.numero_binario = ''.join([bin(int(digit, 16))[2:].zfill(4) for digit in num])  # zfill le ordena que sean 4 bits por cada caracter en hexadecimal
        self.numero_octal = oct(int(self.numero_final, 16))[2:]   
        self.numero_decimal = str(int(self.numero_final, 16))
        self.tabla_numeros.insert("", "end", values=(self.numero_binario, self.numero_octal, self.numero_decimal))#Se insertan los resultados de la conversion en la  tabla correspondiente 
    
    def NRZI(self,num): #Metodo para la grafica de No retorno a cero invertido (NRZI)
        fig, ax = plt.subplots() #Se crea un plot de matplotlib con subplots
        ax.set_xlim(-10, 50) #Define limites inferiores y superiores para los ejes vertical y horizontal 
        ax.set_ylim(-10, 10)
        ax.set_xlabel('Tiempo') #Ubica el tiempo en el eje X y la amplitud de la señal en el eje Y
        ax.set_ylabel('Amplitud')
        ax.set_title('Señal digital con codificación NRZI') #Le da un titulo apropiado a la figura 
        ax.axhline(0, color='black',linewidth=1)  
        ax.set_xticks([])  # Ocultar valores de ejes
        ax.set_yticks([])  
        fig.patch.set_facecolor("#E9E0D6") 
        incremento_x=5 #Define pasos cada 5 unidades entre bit y bit representado graficamente 
        x_actual = -10
        y_actual = 5
        datos_x = []
        datos_y = []
        for i in num:
            if  i=="1": #Si el bit es un 1, lo invierte 
                y_actual = -y_actual
            datos_x.append(x_actual)
            datos_y.append(y_actual)
            x_actual = x_actual+incremento_x #Incrementa el valor de x actual segun el paso definido previamente 
            datos_x.append(x_actual)
            datos_y.append(y_actual)
            ax.axvline(x=x_actual, color='black', linestyle=':')
        ax.plot(datos_x, datos_y) #Plotea los datos almacenadados como pares ordenados 

        for widget in self.frame_NRZI.winfo_children(): #Si el metodo genera widgets residuales,los destruye o elimina 
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_NRZI) #Se crea un nuevo canvas para NRZI a partir del frame anterior 
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.label_eleccion_paridad.config(text="Eliga la paridad que desea aplicar a los datos binarios") #Opcion de elegir el tipo de paridad
        self.boton_paridad_par.config(text="Paridad Par",highlightthickness=2,bd=2, bg="white" ) #Un boton por cada tipo de paridad 
        self.boton_paridad_impar.config(text="Paridad Impar",highlightthickness=2,bd=2, bg="white")
     
       
    def Calculo_bits_paridad(self, cadena_bits): #Metodo para calcular los bits de paridad
            p=0
            while 2**p < (p + len(cadena_bits)+1):
                p= p+1
            self.cantidad_BitsParidad = p
            
    def crear_matriz_binaria(self,bits_paridad):# Crea una matriz binaria de 0 y 1 
            matriz = []
            for i in range(2**bits_paridad):  
                fila = [] 
                num = i
                for j in range(bits_paridad): 
                    fila.insert(0, num % 2)  #Obtiene el bit menos significativo (residuo al dividir la representacion decimal entre 2)
                    num //= 2  #Division entera para obtener el sigiente numero que hay que dividir
                matriz.append(fila)  
            
            self.matriz_paridad = self.Transponer(matriz)

    def Transponer(self, matriz): #Se traspone la matriz binaria, para tener los bits 
        filas = len(matriz)
        columnas = len(matriz[0])
        matriz_transpuesta = []

        for i in range(columnas):  
            sublista = []
            for j in range(filas):  
                sublista.append(matriz[j][i])  
            matriz_transpuesta.append(sublista)

        return matriz_transpuesta

    def Posiciones_paridad(self, matriz):
        n = self.cantidad_BitsParidad  
        for fila in matriz:
            posiciones = [] 
            index = 0  
            for valor in fila:
                if valor == 1 and index<= len(self.numero_binario) + self.cantidad_BitsParidad:  
                    posiciones.append(index-1)  
                index = index + 1  
            posiciones
            
            setattr(self, f"Posiciones_p{n}", posiciones) 
            n = n - 1  
        return

    def Mostrar_posiciones(self):
        print("P5:", self.Posiciones_p5)
        print("P4:", self.Posiciones_p4)
        print("P3:", self.Posiciones_p3)
        print("P2:", self.Posiciones_p2)
        print("P1:", self.Posiciones_p1)
    
    def Paridad_par(self, numero_binario):
        self.reset_paridad
        lista_binario = list(numero_binario)
        for n in range(1, self.cantidad_BitsParidad + 1):
            posicion_paridad = 2**(n-1) - 1  

            posiciones_paridad = getattr(self, f"Posiciones_p{n}")  
            contador_unos = 0
            
            for pos in posiciones_paridad:
                if pos < len(lista_binario) and lista_binario[pos] == "1":
                    contador_unos += 1
            if contador_unos % 2 == 0:
                paridad = 1
            else:
                paridad = 0

            lista_binario[posicion_paridad] = str(paridad)
            setattr(self, f"p{n}", paridad)  
        self.numero_con_paridad = ''.join(lista_binario)
        self.numero_con_error = ''.join(lista_binario)
        self.estado_paridad = "par"

    def Paridad_par_error(self, numero_binario):
            self.reset_paridad
            lista_binario = list(numero_binario)
            for n in range(1, self.cantidad_BitsParidad + 1):
                posicion_paridad = 2**(n-1) - 1  

                posiciones_paridad = getattr(self, f"Posiciones_p{n}")  
                contador_unos = 0
                
                for pos in posiciones_paridad:
                    if pos < len(lista_binario) and lista_binario[pos] == "1":
                        contador_unos += 1
                if contador_unos % 2 == 0:
                    paridad = 1
                else:
                    paridad = 0

                lista_binario[posicion_paridad] = str(paridad)
                setattr(self, f"p{n}", paridad)  
            self.numero_con_paridad = ''.join(lista_binario)
            self.numero_con_error = ''.join(lista_binario)
            self.estado_paridad = "par"


    def Paridad_impar(self, numero_binario):
        self.reset_paridad
        lista_binario = list(numero_binario)
        for n in range(1, self.cantidad_BitsParidad + 1):
            posicion_paridad = 2**(n-1) - 1  

            posiciones_paridad = getattr(self, f"Posiciones_p{n}")  
            contador_unos = 0
            
            for pos in posiciones_paridad:
                if pos < len(lista_binario) and lista_binario[pos] == "1":
                    contador_unos += 1
            if contador_unos % 2 == 0:
                paridad = 0
            else:
                paridad = 1

            lista_binario[posicion_paridad] = str(paridad)
            setattr(self, f"p{n}", paridad)  
        self.numero_con_paridad = ''.join(lista_binario)
        self.estado_paridad = "impar"

    def Paridad_impar_error(self, numero_binario):
            self.reset_paridad
            lista_binario = list(numero_binario)
            for n in range(1, self.cantidad_BitsParidad + 1):
                posicion_paridad = 2**(n-1) - 1  

                posiciones_paridad = getattr(self, f"Posiciones_p{n}")  
                contador_unos = 0
                
                for pos in posiciones_paridad:
                    if pos < len(lista_binario) and lista_binario[pos] == "1":
                        contador_unos += 1
                if contador_unos % 2 == 0:
                    paridad = 0
                else:
                    paridad = 1

                lista_binario[posicion_paridad] = str(paridad)
                setattr(self, f"p{n}", paridad)  
            self.numero_con_error = ''.join(lista_binario)
            self.estado_paridad = "impar"


    def Crear_numero_paridad(self, numero_binario):
        lista_binario = list(numero_binario)
        for i in range(self.cantidad_BitsParidad):
            posicion_paridad = 2**i - 1  
            lista_binario.insert(posicion_paridad, 'p')
        self.placeholder_numero_con_paridad = ''.join(lista_binario)

    def Crear_numero_error(self, numero_binario):
        lista_binario = list(numero_binario)
        for i in range(self.cantidad_BitsParidad):
            posicion_paridad = 2**i - 1  
            lista_binario.insert(posicion_paridad, 'p')
        self.numero_con_error = ''.join(lista_binario)

    def reset_paridad(self):
        try:
            for i in range(1, self.cantidad_BitsParidad + 1):
                delattr(self, f"p{i}")  
        except AttributeError:
                pass
            
    def Mostrar_bits_paridad(self):
        print("P5:", self.p5)
        print("P4:", self.p4)
        print("P3:", self.p3)
        print("P2:", self.p2)
        print("P1:", self.p1)

if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
