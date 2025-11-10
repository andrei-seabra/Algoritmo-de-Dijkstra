from tkinter import *

# Window create/config
window = Tk()
window.geometry("1280x720")
window.title("Algoritmo de Dijkstra")
window.iconphoto(False, PhotoImage(file="assets/icon.png"))

# Main canvas
canvas = Canvas(window, width=1280, height=720)
canvas.pack(fill="both", expand=True)

# Inits app


# Runs app
window.mainloop()