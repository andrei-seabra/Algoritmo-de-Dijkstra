from settings import *
from frontend import *
from tkinter import *

# Window create/config
window = Tk()
window.iconbitmap('assets/icon.ico')
window.resizable(False, False)
window.geometry('1280x720')
window.title('DijkstraLab')

# Menu canvas
menu = Frame(window, width=1280, height=100, bg=LIGHT_TURQUOISE)
menu.grid_rowconfigure(0, weight=1)
menu.grid_columnconfigure(0, weight=1)
menu.pack(fill='x')

logo_image = PhotoImage(file='assets/logo.png')
logo = Label(menu, image=logo_image, bg=LIGHT_TURQUOISE)
logo.pack(side='left', padx=25, pady=20)

# Main canvas
main = Frame(window, width=980, height=620, bg=LIGHT_GRAY)
main.pack_propagate(False)
main.pack(side='left')

# Side bar
side_bar = Frame(window, width=300, height=620, bg=DARK_TURQUOISE)
side_bar.pack_propagate(False)
side_bar.pack(side='right')

create_weight_section(side_bar)
create_animation_section(side_bar, False)
create_dijkstra_section(side_bar)
create_output_section(side_bar)

# Menu buttons
select_button = create_menu_button(menu, 'Selecionar', f'{ICONS_PATH}/cursor.png', lambda: test('selecionar'))
move_button = create_menu_button(menu, 'Mover', f'{ICONS_PATH}/drag.png', lambda: test('mover'))
edge_button = create_menu_button(menu, 'Adicionar aresta', f'{ICONS_PATH}/edge.png', lambda: test('aresta'))
vertex_button = create_menu_button(menu, 'Adicionar nó', f'{ICONS_PATH}/vertex.png', lambda: test('vertice'))
edit_button = create_menu_button(menu, 'Editar aresta', f'{ICONS_PATH}/edit.png', lambda: test('editar'))
delete_button = create_menu_button(menu, 'Apagar', f'{ICONS_PATH}/trash.png', lambda: test('deletar'))
graph_button = create_menu_button(menu, 'Gerar grafo', f'{ICONS_PATH}/graph.png', lambda: test('grafo'))
clean_button = create_menu_button(menu, 'Limpar tudo', f'{ICONS_PATH}/clean.png', lambda: test('limpar'))

# Inits app


# Runs app
window.mainloop()