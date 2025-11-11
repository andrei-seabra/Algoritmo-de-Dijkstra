from tkinter.ttk import Combobox
from settings import *
from tkinter import *
from utils import *

class TopMenu(Frame):
    def __init__(self):
        super().__init__()
        self.configure(width=1280, height=100, bg=LIGHT_TURQUOISE)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.pack(fill='x')

        self.select_button = None
        self.move_button = None
        self.edge_button = None
        self.vertex_button = None
        self.edit_button = None
        self.delete_button = None
        self.graph_button = None
        self.clean_button = None

    def create_logo(self):
        logo_image = PhotoImage(file='assets/logo.png')

        logo = Label(self, image=logo_image, bg=LIGHT_TURQUOISE)
        logo.image = logo_image # Avoids garbage collection
        logo.pack(side='left', padx=25, pady=20)

    def create_button(self, action_text: str, icon: str, action):
        container = Frame(self, bg=LIGHT_TURQUOISE)
        container.pack(side='left', padx=25, pady=20)

        button_image = PhotoImage(file=icon)

        button = Button(container, anchor='center', bd=0, bg=LIGHT_TURQUOISE, activebackground=LIGHT_TURQUOISE, image=button_image, command=action)
        button.image = button_image # Avoids garbage collection
        button.pack()
    
        action_text_label = Label(container, text=action_text, bg=LIGHT_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY)
        action_text_label.pack(pady=(5, 0))

        return button
    
    def create_all_buttons(self):
        self.select_button = self.create_button('Selecionar', f'{ICONS_PATH}/cursor.png', lambda: tool('selecionar'))
        self.move_button = self.create_button('Mover', f'{ICONS_PATH}/drag.png', lambda: tool('mover'))
        self.edge_button = self.create_button('Adicionar aresta', f'{ICONS_PATH}/edge.png', lambda: tool('aresta'))
        self.vertex_button = self.create_button('Adicionar nó', f'{ICONS_PATH}/vertex.png', lambda: tool('vertice'))
        self.edit_button = self.create_button('Editar aresta', f'{ICONS_PATH}/edit.png', lambda: tool('editar'))
        self.delete_button = self.create_button('Apagar', f'{ICONS_PATH}/trash.png', lambda: tool('deletar'))
        self.graph_button = self.create_button('Gerar grafo', f'{ICONS_PATH}/graph.png', lambda: tool('grafo'))
        self.clean_button = self.create_button('Limpar tudo', f'{ICONS_PATH}/clean.png', lambda: tool('limpar'))

    def start(self):
        self.create_logo()
        self.create_all_buttons()



class GraphEditor(Frame):
    def __init__(self):
        super().__init__()
        self.configure(width=980, height=620, bg=LIGHT_GRAY)
        self.pack_propagate(False)
        self.pack(side='left')

        self.debug = 'editor iniciado'

    def start(self):
        print(self.debug)



class Sidebar(Frame):
    def __init__(self):
        super().__init__()
        self.configure(width=300, height=620, bg=DARK_TURQUOISE)
        self.pack_propagate(False)
        self.pack(side='right')

        self.weight_section = None
        self.animation_section = None
        self.dijkstra_section = None
        self.output_section = None

        self.weight_entry = None
        self.animate_checkbutton = None
        self.play_button = None
        self.output_text = None

    def create_section(self, title: str):
        container = Frame(self, bg=DARK_TURQUOISE)
        container.pack()

        label = Label(container, text=title, bg=DARK_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY)
        label.pack(pady=25)

    def create_weight_section(self):
        self.weight_section = self.create_section('Peso padrão')
        
        self.weight_entry = Entry(self, bd=0, bg=LIGHT_TURQUOISE, highlightbackground=LIGHT_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY, justify='center')
        self.weight_entry.insert(0, '1.0')
        self.weight_entry.pack(ipady=7)

    def create_animation_section(self, animate: bool):
        self.animation_section = self.create_section('Passo a passo')

        self.animate_checkbutton = Checkbutton(self, variable=animate, bg=DARK_TURQUOISE, activebackground=DARK_TURQUOISE, selectcolor=LIGHT_TURQUOISE, fg=LIGHT_GRAY, highlightbackground=DARK_TURQUOISE)
        self.animate_checkbutton.pack()

    def create_dijkstra_section(self, options: list):
        self.dijkstra_section = self.create_section('Dijkstra')

        self.vertex_combobox = Combobox(self, background=LIGHT_TURQUOISE, justify='center', font=FONT_FAMILY, textvariable=options[0], values=options, state='readonly')
        self.vertex_combobox.current(0)
        self.vertex_combobox.pack()

        button_image = PhotoImage(file=f'{ICONS_PATH}/play.png')

        self.play_button = Button(self, anchor='center', bd=0, bg=DARK_TURQUOISE, activebackground=DARK_TURQUOISE, image=button_image)
        self.play_button.image = button_image # Avoids garbage collection
        self.play_button.pack(pady=25)

    def create_output_section(self):
        self.output_section = self.create_section('Saída')

        self.output_text = Text(self, bg=LIGHT_TURQUOISE, selectbackground=DARK_TURQUOISE, fg=LIGHT_GRAY, bd=0, font=FONT_FAMILY, wrap='word', state='disabled')
        self.output_text.pack(padx=25, pady=20, expand=True)

    def create_all_sections(self, animate: bool, vertices: list):
        self.create_weight_section()
        self.create_animation_section(animate)
        self.create_dijkstra_section(vertices)
        self.create_output_section()

    def start(self, animate: bool, vertices: list):
        self.create_all_sections(animate, vertices)