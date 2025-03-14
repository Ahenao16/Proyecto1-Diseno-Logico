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

        self.frame = tk.Frame(self.Ventana)  
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.frame.configure(background='#E9E0D6')
        self.label_instrucciones = tk.Label(self.frame, text="Ingrese el número en hexadecimal y presione el botón. Este debe estar formado por 3 caracteres válidos (En el caso de ser un número de dos o un dígito complete el faltante con ceros). Los caracteres numéricos deben ser colocados en minúscula", font=("Arial", 12), fg="Black", anchor = "center",  wraplength=700, bg="#E9E0D6")
        self.label_instrucciones.pack(pady=10)

        self.entry_numero = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_numero.pack(pady=10)

        self.Boton_conversion = tk.Button(self.frame, text="Presionar", command=self.Comprobacion_numero)
        self.Boton_conversion.pack()

        self.label_error = tk.Label(self.frame, text="", font=("Arial", 12), fg="#F25757", bg="#E9E0D6")
        self.label_error.pack(pady=10)

        self.tabla_numeros = ttk.Treeview(self.frame,columns = ('Binario', 'Octal', 'Decimal'), show="headings", height=1, selectmode="none" )
        self.tabla_numeros.heading('Binario', text='Binario (12 bits)')
        self.tabla_numeros.heading('Octal', text='Octal')
        self.tabla_numeros.heading('Decimal', text='Decimal')
        self.tabla_numeros.column('Binario', width=200, anchor='center')  
        self.tabla_numeros.column('Octal', width=200, anchor='center')    
        self.tabla_numeros.column('Decimal', width=200, anchor='center')  
        self.tabla_numeros.pack(pady=10)

        self.formato_tabla_numeros = ttk.Style()
        self.formato_tabla_numeros.configure("Treeview", 
                             font=("Arial", 12),   
                             background="#dcdcdc", 
                             rowheight=25)

        self.formato_tabla_numeros.configure("Treeview.Heading", 
                             font=("Arial", 12, "bold"))
    
        self.frame_NRZI = tk.Frame(self.frame)
        self.frame_NRZI.pack(pady=20)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
