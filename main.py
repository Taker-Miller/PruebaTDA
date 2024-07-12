import tkinter as tk
from gui import SistemaDeAyuda
from login import LoginRegistro

def main():
    root = tk.Tk()
    app = LoginRegistro(root, launch_main_app)
    root.mainloop()

def launch_main_app(tipo_usuario):
    root = tk.Tk()
    app = SistemaDeAyuda(root, tipo_usuario)
    root.mainloop()

if __name__ == "__main__":
    main()
