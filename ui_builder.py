from tkinter.ttk import Combobox
from settings import *
from tkinter import *
from tkinter import simpledialog, messagebox
from utils import *
import math

class TopMenu(Frame):
    def __init__(self, app):
        super().__init__()
        self.configure(width=1280, height=100, bg=LIGHT_TURQUOISE)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.pack(fill='x')

        self.app = app  # Referência ao DijkstraLab

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

    def create_button(self, action_text: str, icon: str, mode: str, action):
        container = Frame(self, bg=LIGHT_TURQUOISE)
        container.pack(side='left', padx=25, pady=20)

        button_image = PhotoImage(file=icon)

        button = Button(container, anchor='center', bd=0, bg=LIGHT_TURQUOISE, activebackground=LIGHT_TURQUOISE, image=button_image, command=action)
        button.image = button_image # Avoids garbage collection
        button.image_path = icon
        button.pack()
        
        action_text_label = Label(container, text=action_text, bg=LIGHT_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY)
        action_text_label.pack(pady=(5, 0))
        button.label = action_text_label

        button.mode = mode

        return button

    def press_button(self, clicked_button: Button):
        buttons = [self.select_button, self.move_button, self.edge_button, self.vertex_button, self.edit_button, self.delete_button]

        for button in buttons:
            if button == clicked_button:
                path = button.image_path.split('/')

                if 'selected_' in path[2]:
                    break

                path[2] = 'selected_' + path[2]
                image_path = '/'.join(path)

                button_image = PhotoImage(file=image_path)
                button.configure(image=button_image)
                button.image_path = image_path
                button.image = button_image

                button.label.configure(fg=LIGHT_BEIGE)
            else:
                path = button.image_path.split('/')

                if path[2].startswith('selected_'):
                    path[2] = path[2].replace('selected_', '', 1)

                image_path = '/'.join(path)
                button_image = PhotoImage(file=image_path)
                button.configure(image=button_image)
                button.image_path = image_path
                button.image = button_image

                button.label.configure(fg=LIGHT_GRAY)

    def create_all_buttons(self):
        self.select_button = self.create_button('Selecionar', f'{ICONS_PATH}/cursor.png', SELECT_MODE, lambda: [self.press_button(self.select_button), self.app.define_mode(SELECT_MODE)])
        self.move_button = self.create_button('Mover', f'{ICONS_PATH}/drag.png', MOVE_MODE, lambda: [self.press_button(self.move_button), self.app.define_mode(MOVE_MODE)])
        self.edge_button = self.create_button('Adicionar aresta', f'{ICONS_PATH}/edge.png', ADD_EDGE, lambda: [self.press_button(self.edge_button), self.app.define_mode(ADD_EDGE)])
        self.vertex_button = self.create_button('Adicionar nó', f'{ICONS_PATH}/vertex.png', ADD_VERTEX, lambda: [self.press_button(self.vertex_button), self.app.define_mode(ADD_VERTEX)])
        self.edit_button = self.create_button('Editar aresta', f'{ICONS_PATH}/edit.png', EDIT_EDGE, lambda: [self.press_button(self.edit_button), self.app.define_mode(EDIT_EDGE)])
        self.delete_button = self.create_button('Apagar', f'{ICONS_PATH}/trash.png', DELETE_MODE, lambda: [self.press_button(self.delete_button), self.app.define_mode(DELETE_MODE)])
        self.graph_button = self.create_button('Gerar grafo', f'{ICONS_PATH}/graph.png', '', lambda: self.app.generate_graph())
        self.clean_button = self.create_button('Limpar tudo', f'{ICONS_PATH}/clean.png', '', lambda: self.app.clear_all())

    def start(self):
        self.create_logo()
        self.create_all_buttons()



class GraphEditor(Frame):
    def __init__(self, app):
        super().__init__()
        self.configure(width=980, height=620, bg=LIGHT_GRAY)
        self.pack_propagate(False)
        self.pack(side='left')

        self.app = app  # Referência ao DijkstraLab
        self.canvas = None

    def start(self):
        # Cria o canvas
        self.canvas = Canvas(self, width=980, height=620, bg='white')
        self.canvas.pack(fill='both', expand=True)
        
        # Bind eventos
        self.canvas.bind('<Button-1>', lambda e: self.detect_click(e, self.app.mode))
        self.canvas.bind('<B1-Motion>', self.detect_drag)
        self.canvas.bind('<ButtonRelease-1>', self.detect_release)
        
        self.redraw_all()

    def detect_click(self, event, mode: str):
        x, y = event.x, event.y

        if mode == SELECT_MODE:
            lbl = self.find_vertex(x, y)
            if lbl and self.app.sidebar:
                self.show_node_info(lbl)
                
        elif mode == ADD_VERTEX:
            self.create_vertex(x, y)
            
        elif mode == ADD_EDGE:
            lbl = self.find_vertex(x, y)
            if not lbl:
                return
            if self.app.selected_for_edge is None:
                self.app.selected_for_edge = lbl
            else:
                if self.app.selected_for_edge != lbl:
                    w = self.app.default_weight
                    try:
                        if self.app.sidebar and self.app.sidebar.weight_entry:
                            w = float(self.app.sidebar.weight_entry.get())
                    except:
                        w = self.app.default_weight
                    self.create_edge(self.app.selected_for_edge, lbl, w)
                    # Se não for direcionado, cria aresta reversa
                    if not self.app.directed:
                        self.create_edge(lbl, self.app.selected_for_edge, w)
                self.app.selected_for_edge = None
                
        elif mode == MOVE_MODE:
            lbl = self.find_vertex(x, y)
            if lbl:
                self.app.dragging_node = lbl
                
        elif mode == DELETE_MODE:
            lbl = self.find_vertex(x, y)
            if lbl:
                self.delete_vertex(lbl)
            else:
                edge = self.find_edge(x, y)
                if edge:
                    self.delete_edge(edge[0], edge[1])
                    # Se não for direcionado, remove aresta reversa
                    if not self.app.directed:
                        self.delete_edge(edge[1], edge[0])
                    
        elif mode == EDIT_EDGE:
            edge = self.find_edge(x, y)
            if edge:
                u, v = edge
                try:
                    current_w = self.get_edge_weight(u, v) or 1.0

                    alert_box = Tk()
                    alert_box.iconbitmap('assets/icon.ico')
                    alert_box.resizable(False, False)
                    alert_box.geometry('320x180')
                    alert_box.title('DijkstraLab')

                    container = Frame(alert_box, bg=LIGHT_TURQUOISE)
                    container.pack(fill='both', expand=True)

                    label = Label(container, font=FONT_FAMILY, text=f'Editar peso\nPeso para {u} -> {v}', bg=LIGHT_TURQUOISE, fg=LIGHT_GRAY)
                    label.grid(row=0, column=0, padx=90, pady=15)

                    def close_alert():
                        new_w = float(weight_entry.get())
                        alert_box.destroy()

                        if new_w is not None:
                            self.set_edge_weight(u, v, float(new_w))
                            # Se não for direcionado, atualiza aresta reversa
                            if not self.app.directed:
                                self.set_edge_weight(v, u, float(new_w))

                    weight_entry = Entry(container, bd=0, bg=DARK_TURQUOISE, highlightbackground=DARK_TURQUOISE, fg=LIGHT_GRAY, font=FONT_FAMILY, justify='center')
                    weight_entry.insert(0, current_w)
                    
                    weight_entry.grid(row=1, column=0, padx=90, pady=20)

                    button = Button(container, text='Ok', bd=0, font=FONT_FAMILY, fg=LIGHT_GRAY, activeforeground=LIGHT_GRAY, bg=DARK_TURQUOISE, activebackground=DARK_TURQUOISE, command=close_alert)
                    button.grid(row=2, column=0, padx=90, ipadx=15, ipady=7)

                    alert_box.mainloop()
                except:
                    pass
        
    def detect_drag(self, event):
        if self.app.mode == MOVE_MODE and self.app.dragging_node:
            x, y = event.x, event.y
            x = max(NODE_RAY, min(980 - NODE_RAY, x))
            y = max(NODE_RAY, min(620 - NODE_RAY, y))
            self.app.nodes[self.app.dragging_node]['pos'] = (x, y)
            self.redraw_all()

    def detect_release(self, event):
        self.app.dragging_node = None

    def create_vertex(self, x: int, y: int):
        label = self.next_label()
        x = max(NODE_RAY, min(980 - NODE_RAY, x))
        y = max(NODE_RAY, min(620 - NODE_RAY, y))
        self.app.nodes[label] = {'pos': (x, y)}
        
        if self.app.sidebar:
            self.app.sidebar.update_vertices(self.get_vertex_labels())
        
        self.redraw_all()

    def next_label(self):
        i = self.app.next_node_id
        s = ''
        while True:
            s = chr(ord('A') + ((i - 1) % 26)) + s
            i = (i - 1) // 26
            if i <= 0:
                break
        self.app.next_node_id += 1
        return s

    def delete_vertex(self, lbl):
        self.app.edges = [e for e in self.app.edges if e['u'] != lbl and e['v'] != lbl]
        if lbl in self.app.nodes:
            del self.app.nodes[lbl]
        
        if self.app.sidebar:
            self.app.sidebar.update_vertices(self.get_vertex_labels())
        
        self.redraw_all()

    def find_vertex(self, x: int, y: int):
        for lbl, data in self.app.nodes.items():
            nx, ny = data['pos']
            if (x - nx) ** 2 + (y - ny) ** 2 <= NODE_RAY ** 2:
                return lbl
        return None

    def create_edge(self, u, v, w):
        w = float(w)
        # Atualiza se existir, senão adiciona
        for e in self.app.edges:
            if e['u'] == u and e['v'] == v:
                return
        self.app.edges.append({'u': u, 'v': v, 'w': w})
        self.redraw_all()

    def delete_edge(self, u, v):
        self.app.edges = [e for e in self.app.edges if not (e['u'] == u and e['v'] == v)]
        self.redraw_all()

    def set_edge_weight(self, u, v, w):
        for e in self.app.edges:
            if e['u'] == u and e['v'] == v:
                e['w'] = float(w)
                self.redraw_all()
                return
        self.create_edge(u, v, w)

    def get_edge_weight(self, u, v):
        for e in self.app.edges:
            if e['u'] == u and e['v'] == v:
                return e['w']
        return None

    def find_edge(self, x: int, y: int):
        for e in self.app.edges:
            u, v = e['u'], e['v']
            if u not in self.app.nodes or v not in self.app.nodes:
                continue
            x1, y1 = self.app.nodes[u]['pos']
            x2, y2 = self.app.nodes[v]['pos']
            
            if self._dist_point_to_segment(x, y, x1, y1, x2, y2) <= 8:
                return (u, v)
        return None

    @staticmethod
    def _dist_point_to_segment(px, py, x1, y1, x2, y2):
        """Calcula a distância de um ponto a um segmento de reta."""
        dx = x2 - x1
        dy = y2 - y1
        if dx == dy == 0:
            return math.hypot(px - x1, py - y1)
        t = ((px - x1) * dx + (py - y1) * dy) / (dx*dx + dy*dy)
        t = max(0, min(1, t))
        projx = x1 + t * dx
        projy = y1 + t * dy
        return math.hypot(px - projx, py - projy)

    def get_vertex_labels(self):
        return sorted(list(self.app.nodes.keys()))

    def show_node_info(self, lbl):
        if not self.app.sidebar:
            return
        
        outs = [e for e in self.app.edges if e['u'] == lbl]
        ins = [e for e in self.app.edges if e['v'] == lbl]
        
        info = f"Nó: {lbl}\n"
        info += f"Pos: ({self.app.nodes[lbl]['pos'][0]:.0f}, {self.app.nodes[lbl]['pos'][1]:.0f})\n\n"
        info += f"Saídas ({len(outs)}):\n"
        for e in outs:
            info += f"  -> {e['v']} (peso={e['w']})\n"
        info += f"\nEntradas ({len(ins)}):\n"
        for e in ins:
            info += f"  <- {e['u']} (peso={e['w']})\n"
        
        self.app.sidebar.output_text.config(state='normal')
        self.app.sidebar.output_text.delete('1.0', END)
        self.app.sidebar.output_text.insert(END, info)
        self.app.sidebar.output_text.config(state='disabled')

    def redraw_all(self):
        if not self.canvas:
            return
        
        self.canvas.delete('all')
        self.app.node_art.clear()
        self.app.edge_art.clear()

        # Construir conjunto de arestas no caminho mínimo
        path_edges = set()
        if self.app.last_prev and self.app.last_source:
            for dest in self.app.nodes.keys():
                if dest != self.app.last_source:
                    # Reconstrói caminho
                    path = []
                    cur = dest
                    while cur is not None:
                        path.append(cur)
                        cur = self.app.last_prev.get(cur)
                    
                    # Adiciona arestas do caminho
                    for i in range(len(path) - 1):
                        path_edges.add((path[i+1], path[i]))

        # Desenha arestas
        for e in self.app.edges:
            u, v = e['u'], e['v']
            if u not in self.app.nodes or v not in self.app.nodes:
                continue
            x1, y1 = self.app.nodes[u]['pos']
            x2, y2 = self.app.nodes[v]['pos']
            w = e['w']
            
            # Verifica se esta aresta faz parte do caminho mínimo
            is_path_edge = (u, v) in path_edges
            edge_color = '#00AA00' if is_path_edge else 'gray'
            edge_width = 3 if is_path_edge else EDGE_WIDTH
            
            # Calcular ponto de deslocamento para evitar que a linha toque o centro do nó
            angle = math.atan2(y2 - y1, x2 - x1)
            dx_r = NODE_RAY * math.cos(angle)
            dy_r = NODE_RAY * math.sin(angle)
            
            start_x = x1 + dx_r
            start_y = y1 + dy_r
            end_x = x2 - dx_r
            end_y = y2 - dy_r
            
            # Linha com seta (ou sem seta se não for direcionado)
            arrow_style = LAST if self.app.directed else NONE
            line = self.canvas.create_line(start_x, start_y, end_x, end_y, 
                                          width=edge_width, fill=edge_color, arrow=arrow_style)
            
            # Posição do peso (texto)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            
            # Deslocamento do texto para o lado da aresta
            offset_dist = 12
            text_x = mx + offset_dist * math.sin(angle)
            text_y = my - offset_dist * math.cos(angle)
            
            text_color = '#006600' if is_path_edge else 'black'
            text = self.canvas.create_text(text_x, text_y, text=str(w), 
                                          font=FONT_FAMILY, fill=text_color)
            self.app.edge_art[(u, v)] = (line, text)

        # Desenha nós
        for lbl, data in self.app.nodes.items():
            x, y = data['pos']
            fill_color = 'lightgreen' if lbl == self.app.last_source else LIGHT_BEIGE
            
            oval = self.canvas.create_oval(x - NODE_RAY, y - NODE_RAY, 
                                          x + NODE_RAY, y + NODE_RAY, 
                                          fill=fill_color, outline='black', width=2)
            text = self.canvas.create_text(x, y, text=lbl, font=FONT_FAMILY, fill='black')
            self.app.node_art[lbl] = (oval, text)

        # Desenha info de modo
        mode_text = self.app.mode if self.app.mode else 'Nenhum'
        graph_type = 'Não Direcionado' if not self.app.directed else 'Direcionado'
        self.canvas.create_text(10, 600, anchor='w', text=f"Modo: {mode_text} | Tipo: {graph_type}", 
                               font=('Arial', 9, 'italic'), fill='darkred')



class Sidebar(Frame):
    def __init__(self, app):
        super().__init__()
        self.configure(width=300, height=620, bg=DARK_TURQUOISE)
        self.pack_propagate(False)
        self.pack(side='right')

        self.app = app  # Referência ao DijkstraLab

        self.weight_section = None
        self.animation_section = None
        self.dijkstra_section = None
        self.output_section = None

        self.weight_entry = None
        self.animate_checkbutton = None
        self.play_button = None
        self.output_text = None
        self.source_var = None
        self.vertex_combobox = None

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

    def create_direction_section(self, directed: bool):
        self.direction_section = self.create_section('Direcionado')
        
        self.directed_var = BooleanVar(value=directed)
        self.directed_checkbutton = Checkbutton(self, variable=self.directed_var, 
                                               command=self._on_directed_change,
                                               bg=DARK_TURQUOISE, activebackground=DARK_TURQUOISE, 
                                               selectcolor=LIGHT_TURQUOISE, fg=LIGHT_GRAY, 
                                               highlightbackground=DARK_TURQUOISE)
        self.directed_checkbutton.pack()

    def _on_directed_change(self):
        """Callback quando o checkbox de direcionado muda."""
        self.app.directed = self.directed_var.get()
        if self.app.graph_editor:
            self.app.graph_editor.redraw_all()

        self.app.clear_all()

    def create_dijkstra_section(self, vertices: list):
        self.dijkstra_section = self.create_section('Dijkstra')

        self.source_var = StringVar()
        self.vertex_combobox = Combobox(self, background=LIGHT_TURQUOISE, justify='center', font=FONT_FAMILY, 
                                       textvariable=self.source_var, values=vertices, state='readonly')
        if vertices:
            self.source_var.set(vertices[0])
        self.vertex_combobox.pack()

        button_image = PhotoImage(file=f'{ICONS_PATH}/play.png')

        self.play_button = Button(self, anchor='center', bd=0, bg=DARK_TURQUOISE, activebackground=DARK_TURQUOISE, 
                                 image=button_image, command=self.app.run_dijkstra)
        self.play_button.image = button_image # Avoids garbage collection
        self.play_button.pack(pady=25)

    def create_output_section(self):
        self.output_section = self.create_section('Saída')

        self.output_text = Text(self, bg=LIGHT_TURQUOISE, selectbackground=DARK_TURQUOISE, fg=LIGHT_GRAY, bd=0, font=FONT_FAMILY, wrap='word', state='disabled')
        self.output_text.pack(padx=25, pady=20, expand=True)

    def create_all_sections(self, directed: bool, vertices: list):
        self.create_weight_section()
        self.create_direction_section(directed)
        self.create_dijkstra_section(vertices)
        self.create_output_section()

    def start(self, directed: bool, vertices: list):
        self.create_all_sections(directed, vertices)

    def update_vertices(self, vertices: list):
        """Atualiza a lista de vértices no combobox."""
        try:
            self.vertex_combobox['values'] = vertices
            if vertices and not self.source_var.get():
                self.source_var.set(vertices[0])
        except:
            pass

    def clear_output(self):
        """Limpa a área de saída."""
        try:
            self.output_text.config(state='normal')
            self.output_text.delete('1.0', END)
            self.output_text.config(state='disabled')
        except:
            pass