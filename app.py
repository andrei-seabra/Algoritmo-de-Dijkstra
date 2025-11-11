from ui_builder import TopMenu, GraphEditor, Sidebar
from tkinter import *

class DijkstraLab(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('assets/icon.ico')
        self.resizable(False, False)
        self.geometry('1280x720')
        self.title('DijkstraLab')

        self.animate = False
        self.vertices = ['A']

    def start(self):
        top_menu = TopMenu()
        top_menu.start()

        graph_editor = GraphEditor()
        graph_editor.start()

        sidebar = Sidebar()
        sidebar.start(self.animate, self.vertices)

        self.mainloop()