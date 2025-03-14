import tkinter as tk

class Interfaz:
    def __init__(self, Ventana):
        self.Diccionario_valido = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f")
        self.Ventana = Ventana
        self.Ventana.title("Código Hamming")
        self.Ventana.geometry("800x800")
        self.Ventana.resizable(False, False)
        self.numero_final = "" 

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

    def Comprobacion_numero(self):
        diccionario = self.Diccionario_valido
        numero_comprobacion = self.entry_numero.get()

        if len(numero_comprobacion) != 3:
            self.label_error.config(text="El número debe tener exactamente 3 caracteres.", fg= "Red")
            return

        for i in numero_comprobacion:
            if i not in diccionario:
                self.label_error.config(text="El número debe estar formado por caracteres válidos.", fg= "Red")
                return

        self.Obtener_numero()

    def Obtener_numero(self):
        self.numero_final = self.entry_numero.get()
        self.label_error.config(text="Usted ingresó el número: " + self.numero_final, fg="Green")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
