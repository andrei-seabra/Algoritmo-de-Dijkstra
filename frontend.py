from tkinter.ttk import Combobox
from settings import *
from tkinter import *

def create_menu_button(menu: Frame, action_text: str, icon: str, action):
    container = Frame(menu, bg=LIGHT_TURQUOISE)
    container.pack(side='left', padx=25, pady=20)

    button_image = PhotoImage(file=icon)

    button = Button(container, anchor='center', bd=0, bg=LIGHT_TURQUOISE, activebackground=LIGHT_TURQUOISE, image=button_image, command=action)
    button.image = button_image # Avoids garbage collection
    button.pack()
    
    action_text_label = Label(container, text=action_text, bg=LIGHT_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY)
    action_text_label.pack(pady=(5, 0))

    return button

def test(action: str):
    print(f'{action}')

def create_weight_section(side_bar: Frame):
    weight_section = Frame(side_bar, bg=DARK_TURQUOISE)
    weight_section.pack()

    title_label = Label(weight_section, text='Peso padrão', bg=DARK_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY)
    title_label.pack(pady=25)

    weight_entry = Entry(side_bar, bd=0, bg=LIGHT_TURQUOISE, highlightbackground=LIGHT_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY, justify='center')
    weight_entry.insert(0, '1.0')
    weight_entry.pack(ipady=7)

def create_animation_section(side_bar: Frame, animate: bool):
    dijkstra_section = Frame(side_bar, bg=DARK_TURQUOISE)
    dijkstra_section.pack()

    title_label = Label(dijkstra_section, text='Passo a passo', bg=DARK_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY)
    title_label.pack(pady=25)

    checkbox = Checkbutton(side_bar, variable=animate, bg=DARK_TURQUOISE, activebackground=DARK_TURQUOISE, selectcolor=LIGHT_TURQUOISE, fg=LIGHT_GRAY, highlightbackground=DARK_TURQUOISE)
    checkbox.pack()

def create_dijkstra_section(side_bar: Frame):
    dijkstra_section = Frame(side_bar, bg=DARK_TURQUOISE)
    dijkstra_section.pack()

    title_label = Label(dijkstra_section, text='Dijkstra', bg=DARK_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY)
    title_label.pack(pady=25)

    options = ['A', 'B', 'C', 'D']

    drop_down_vertex = Combobox(dijkstra_section, background=LIGHT_TURQUOISE, justify='center', font=FONT_FAMILY, textvariable=options[0], values=options, state='readonly')
    drop_down_vertex.current(0)
    drop_down_vertex.pack()

    button_image = PhotoImage(file=f'{ICONS_PATH}/play.png')

    button = Button(dijkstra_section, anchor='center', bd=0, bg=DARK_TURQUOISE, activebackground=DARK_TURQUOISE, image=button_image)
    button.image = button_image
    button.pack(pady=25)

def create_output_section(side_bar: Frame):
    output_section = Frame(side_bar, bg=DARK_TURQUOISE)
    output_section.pack()

    title_label = Label(output_section, text='Saída', bg=DARK_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY)
    title_label.pack()

    output_text = Text(side_bar, bg=LIGHT_TURQUOISE, selectbackground=DARK_TURQUOISE, fg=LIGHT_GRAY, bd=0, font=FONT_FAMILY, wrap='word', state='disabled')
    output_text.pack(padx=25, pady=25, expand=True)

def clean_frame(frame: Frame):
    for widget in frame.winfo_children():
        widget.destroy()