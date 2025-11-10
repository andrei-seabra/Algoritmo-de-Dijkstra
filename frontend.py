from tkinter import *

def clean_canvas(canvas: Canvas):
    for widget in canvas.find_all():
        canvas.delete(widget)