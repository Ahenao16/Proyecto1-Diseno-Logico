import tkinter as tk
from tkinter import ttk

class Interfaz:
    def __init__(self, Ventana):
        self.Diccionario_valido = ("0","1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f")
        self.Ventana = Ventana
        self.Ventana.title("Código Hamming")
        self.Ventana.geometry("800x800")
        self.Ventana.resizable(False, False)
        self.numero_final = "" 
        self.numero_binario = ""
        self.numero_octal = ""
        self.numero_decimal = ""

        self.frame = tk.Frame(self.Ventana)  
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label_instrucciones = tk.Label(self.frame, text="Ingrese el número en hexadecimal y presione el botón. Este debe estar formado por 3 caracteres válidos (En el caso de ser un número de dos o un dígito complete el faltante con ceros). Los caracteres numéricos deben ser colocados en minúscula", font=("Arial", 12), fg="Black", anchor = "center",  wraplength=700)
        self.label_instrucciones.pack(pady=10)

        self.entry_numero = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_numero.pack(pady=10)

        self.Boton_conversion = tk.Button(self.frame, text="Presionar", command=self.Comprobacion_numero)
        self.Boton_conversion.pack()

        self.label_error = tk.Label(self.frame, text="", font=("Arial", 12), fg="red")
        self.label_error.pack(pady=10)

        self.tabla_numeros = ttk.Treeview(self.frame,columns = ('Binario', 'Octal', 'Decimal'), show="headings", height=1 )
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
    

    def Comprobacion_numero(self):
        diccionario = self.Diccionario_valido
        numero_comprobacion = self.entry_numero.get()

        if len(numero_comprobacion) != 3:
            self.label_error.config(text="El número debe tener exactamente 3 caracteres. Intente de nuevo.", fg= "Red")
            return

        for i in numero_comprobacion:
            if i not in diccionario:
                self.label_error.config(text="El número debe estar formado por caracteres válidos. Intente de nuevo", fg= "Red")
                return

        self.Obtener_numero()
        self.Conversor(self.numero_final)

    def Obtener_numero(self):
        self.numero_final = self.entry_numero.get()
        self.label_error.config(text="Usted ingresó el número hexadecimal: " + self.numero_final, fg="Green")
        return self.numero_final

    def Conversor(self,num):
        for item in self.tabla_numeros.get_children():  #Esto es para eliminar la tabla al darle 2 veces al boton
            self.tabla_numeros.delete(item)

        self.numero_binario = ''.join([bin(int(digit, 16))[2:].zfill(4) for digit in num])  #zfill le ordena que sean 4 bits por cada caracter en hexadecimal
        self.numero_octal = oct(int(self.numero_final, 16))[2:]   
        self.numero_decimal = str(int(self.numero_final, 16))
        self.tabla_numeros.insert("", "end", values=(self.numero_binario, self.numero_octal, self.numero_decimal))

if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
