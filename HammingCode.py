import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Interfaz:
    def __init__(self, Ventana):
        self.Diccionario_valido = ("0","1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f")
        self.Ventana = Ventana
        self.Ventana.title("Código Hamming")
        self.Ventana.geometry("800x800")
        self.Ventana.resizable(False, False)
        self.Ventana.configure(bg="#E9E0D6")
        self.numero_final = "" 
        self.numero_binario = ""
        self.numero_octal = ""
        self.numero_decimal = ""
        self.cantidad_BitsParidad = 0
        self.matriz_paridad = []
        self.numero_con_paridad = ""
        self.numero_con_error ="" 
        self.bit_error = ""

  
        self.canvas = tk.Canvas(self.Ventana, bg="#E9E0D6")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = tk.Scrollbar(self.Ventana, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
    
        self.canvas.config(yscrollcommand=self.scrollbar.set)

  
        self.frame = tk.Frame(self.canvas, bg="#E9E0D6")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

      
        self.frame.bind("<Configure>", self.on_frame_configure)

   
        self.label_instrucciones = tk.Label(self.frame, text="Ingrese el número en hexadecimal y presione el botón. Este debe estar formado por 3 caracteres válidos (En el caso de ser un número de dos o un dígito complete el faltante con ceros). Los caracteres numéricos deben ser colocados en minúscula", font=("Arial", 12), fg="Black", anchor="center", wraplength=700, bg="#E9E0D6")
        self.label_instrucciones.pack(pady=10, padx=50)

        self.entry_numero = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_numero.pack(pady=10, padx=50)

        self.Boton_conversion = tk.Button(self.frame, text="Presionar", command=self.Comprobacion_numero ,highlightthickness=2,bd=2, bg="white")
        self.Boton_conversion.pack(pady=10, padx=50)

        self.label_error = tk.Label(self.frame, text="", font=("Arial", 12), fg="#F25757", bg="#E9E0D6")
        self.label_error.pack(pady=10, padx=50)

        self.tabla_numeros = ttk.Treeview(self.frame, columns=('Binario', 'Octal', 'Decimal'), show="headings", height=1, selectmode="none")
        self.tabla_numeros.heading('Binario', text='Binario (12 bits)')
        self.tabla_numeros.heading('Octal', text='Octal')
        self.tabla_numeros.heading('Decimal', text='Decimal')
        self.tabla_numeros.column('Binario', width=200, anchor='center')
        self.tabla_numeros.column('Octal', width=200, anchor='center')
        self.tabla_numeros.column('Decimal', width=200, anchor='center')
        self.tabla_numeros.pack(pady=10, padx=50)

        self.formato_tabla_numeros = ttk.Style()
        self.formato_tabla_numeros.configure("Treeview", font=("Arial", 12), background="#dcdcdc", rowheight=25)
        self.formato_tabla_numeros.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        
        self.frame_NRZI = tk.Frame(self.frame)
        self.frame_NRZI.pack(pady=5, padx=50)

        self.label_eleccion_paridad = tk.Label(self.frame, text="", font=("Arial", 12), bg="#E9E0D6")
        self.label_eleccion_paridad.pack(pady=5, padx=50)

        self.boton_paridad_par= tk.Button(self.frame, text="", font=("Arial", 12), bg="#E9E0D6",bd=0, highlightthickness=0,command=lambda:self.Llamada_paridad_par())
        self.boton_paridad_par.pack(side="left", padx=185,pady=5)

        self.boton_paridad_impar= tk.Button(self.frame, text="", font=("Arial", 12), bg="#E9E0D6",bd=0, highlightthickness=0,command=lambda:self.Llamada_paridad_impar())
        self.boton_paridad_impar.pack(side="left")

    def on_frame_configure(self, event=None):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def Comprobacion_numero(self):
        diccionario = self.Diccionario_valido
        numero_comprobacion = self.entry_numero.get()

        if len(numero_comprobacion) != 3:
            self.label_error.config(text="El número debe tener exactamente 3 caracteres. Intente de nuevo.", fg= "#F25757")
            return

        for i in numero_comprobacion:
            if i not in diccionario:
                self.label_error.config(text="El número debe estar formado por caracteres válidos. Intente de nuevo", fg= "#F25757")
                return

        self.Obtener_numero()
        self.Conversor(self.numero_final)
        self.NRZI(self.numero_binario)
        self.Calculo_bits_paridad(self.numero_binario)
        self.crear_matriz_binaria(self.cantidad_BitsParidad)
        self.Posiciones_paridad(self.matriz_paridad)
        self.Mostrar_posiciones()
        self.Crear_numero_paridad(self.numero_binario)
        print(self.matriz_paridad)
        print(self.numero_con_paridad)
        print(len(self.numero_con_paridad))

    def Llamada_paridad_par(self):
        self.Paridad_par(self.numero_con_paridad)
        self.Mostrar_bits_paridad()
        print(self.numero_con_paridad)
        self.Revisar_error_par("00010101001010101")
        print(self.bit_error)

    def Llamada_paridad_impar(self):
        self.Paridad_impar(self.numero_con_paridad)
        self.Mostrar_bits_paridad()
        print(self.numero_con_paridad)
      

    def Obtener_numero(self):
        self.numero_final = self.entry_numero.get()
        self.label_error.config(text="Usted ingresó el número hexadecimal: " + self.numero_final, fg="#4EA699")
        return self.numero_final

    def Conversor(self,num):
        for item in self.tabla_numeros.get_children():  # Esto es para eliminar la tabla al darle 2 veces al boton
            self.tabla_numeros.delete(item)

        self.numero_binario = ''.join([bin(int(digit, 16))[2:].zfill(4) for digit in num])  # zfill le ordena que sean 4 bits por cada caracter en hexadecimal
        self.numero_octal = oct(int(self.numero_final, 16))[2:]   
        self.numero_decimal = str(int(self.numero_final, 16))
        self.tabla_numeros.insert("", "end", values=(self.numero_binario, self.numero_octal, self.numero_decimal))
    
    def NRZI(self,num):
        fig, ax = plt.subplots()
        ax.set_xlim(-10, 50)
        ax.set_ylim(-10, 10)
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Amplitud')
        ax.set_title('Señal digital con codificación NRZI')
        ax.axhline(0, color='black',linewidth=1)  
        ax.set_xticks([])  # Ocultar valores de ejes
        ax.set_yticks([])  
        fig.patch.set_facecolor("#E9E0D6") 
        incremento_x=5
        x_actual = -10
        y_actual = 5
        datos_x = []
        datos_y = []
        for i in num:
            if  i=="1":
                y_actual = -y_actual
            datos_x.append(x_actual)
            datos_y.append(y_actual)
            x_actual = x_actual+incremento_x
            datos_x.append(x_actual)
            datos_y.append(y_actual)
            ax.axvline(x=x_actual, color='black', linestyle=':')
        ax.plot(datos_x, datos_y)

        for widget in self.frame_NRZI.winfo_children(): 
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_NRZI)
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.label_eleccion_paridad.config(text="Eliga la paridad que desea aplicar a los datos binarios")
        self.boton_paridad_par.config(text="Paridad Par",highlightthickness=2,bd=2, bg="white" )
        self.boton_paridad_impar.config(text="Paridad Impar",highlightthickness=2,bd=2, bg="white")
     
       
        

    def Calculo_bits_paridad(self, cadena_bits):
            p=0
            while 2**p < (p + len(cadena_bits)+1):
                p= p+1
            self.cantidad_BitsParidad = p
            
    def crear_matriz_binaria(self,bits_paridad):
            matriz = []
            for i in range(2**bits_paridad):  
                fila = [] 
                num = i
                for j in range(bits_paridad): 
                    fila.insert(0, num % 2)  #Obtengo el bit menos significativo (residuo al dividir la representacion decimal entre 2)
                    num //= 2  #Division entera para obtener el sigiente numero que hay que dividir
                matriz.append(fila)  
            
            self.matriz_paridad = self.Transponer(matriz)

    def Transponer(self, matriz):
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
            posiciones= posiciones[1:]
            
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


    def Paridad_impar(self, numero_binario):
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


    def Revisar_error_par(self, numero_binario):
        lista_binario = list(numero_binario)
        bit_error_posicion = 0  
        error_posicion_binario = []  

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

            if posicion_paridad < len(lista_binario) and int(lista_binario[posicion_paridad]) != paridad:
                error_posicion_binario.append('1') 
            else:
                error_posicion_binario.append('0')  

        bit_error_posicion = ''.join(error_posicion_binario)  

        
        self.bit_error = bit_error_posicion  
        return self.bit_error


    def Crear_numero_paridad(self, numero_binario):
        lista_binario = list(numero_binario)
        for i in range(self.cantidad_BitsParidad):
            posicion_paridad = 2**i - 1  
            lista_binario.insert(posicion_paridad, 'p')
        self.numero_con_paridad = ''.join(lista_binario)


            
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
