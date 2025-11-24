from ui_builder import TopMenu, GraphEditor, Sidebar
from tkinter import *
from settings import *
from tkinter import messagebox
from utils import dijkstra
import random

class DijkstraLab(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('assets/icon.ico')
        self.resizable(False, False)
        self.geometry('1280x720')
        self.title('DijkstraLab')

        # Configuration
        self.mode = None
        self.animate = False
        self.selected_for_edge = None
        self.dragging_node = None
        self.directed = False
        self.default_weight = 1
        
        # Graph Data Structure
        self.nodes = {}
        self.edges = []
        self.next_node_id = 1

        # ID Mapping
        self.node_art = {}
        self.edge_art = {}

        # Dijkstra State
        self.last_dist = {}
        self.last_prev = {}
        self.last_source = None
        self.label_to_id = {}
        
        # Componentes UI
        self.top_menu = None
        self.graph_editor = None
        self.sidebar = None

    def define_mode(self, mode: str):
        self.mode = mode

    def generate_graph(self):
        """Gera um grafo aleatório."""
        self.clear_all()
        
        # Número aleatório de nós (entre 4 e 8)
        num_nodes = random.randint(4, 8)
        
        # Gera posições aleatórias para os nós, evitando sobreposição
        labels = []
        margin = 60
        min_distance = 100  # Distância mínima entre nós
        
        for _ in range(num_nodes):
            attempts = 0
            while attempts < 50:  # Tenta 50 vezes para encontrar uma posição válida
                x = random.randint(margin, 980 - margin)
                y = random.randint(margin, 620 - margin)
                
                # Verifica se está longe o suficiente dos outros nós
                valid = True
                for other_label in labels:
                    ox, oy = self.nodes[other_label]['pos']
                    dist = ((x - ox)**2 + (y - oy)**2)**0.5
                    if dist < min_distance:
                        valid = False
                        break
                
                if valid:
                    # Gera label
                    i = self.next_node_id - 1
                    s = ''
                    while True:
                        s = chr(ord('A') + (i % 26)) + s
                        i = i // 26 - 1
                        if i < 0:
                            break
                    self.next_node_id += 1
                    
                    self.nodes[s] = {'pos': (x, y)}
                    labels.append(s)
                    break
                
                attempts += 1
            
            # Se não conseguiu achar posição válida após 50 tentativas, coloca em grade
            if attempts >= 50:
                i = self.next_node_id - 1
                s = ''
                while True:
                    s = chr(ord('A') + (i % 26)) + s
                    i = i // 26 - 1
                    if i < 0:
                        break
                self.next_node_id += 1
                
                row = len(labels) // 3
                col = len(labels) % 3
                x = 150 + col * 250
                y = 150 + row * 200
                self.nodes[s] = {'pos': (x, y)}
                labels.append(s)
        
        # Gera arestas aleatórias
        # Garante conectividade criando uma árvore geradora primeiro
        available = labels[1:]
        connected = [labels[0]]
        
        while available:
            # Conecta um nó disponível a um nó já conectado
            u = random.choice(connected)
            v = available.pop(random.randint(0, len(available) - 1))
            w = round(random.uniform(0.5, 5.0), 1)
            
            self.edges.append({'u': u, 'v': v, 'w': w})
            if not self.directed:
                self.edges.append({'u': v, 'v': u, 'w': w})
            
            connected.append(v)
        
        # Adiciona arestas extras aleatórias (30-60% de arestas extras possíveis)
        max_extra_edges = (num_nodes * (num_nodes - 1)) // 2 - (num_nodes - 1)
        num_extra = random.randint(int(max_extra_edges * 0.3), int(max_extra_edges * 0.6))
        
        for _ in range(num_extra):
            u = random.choice(labels)
            v = random.choice(labels)
            
            # Evita auto-loops e arestas duplicadas
            if u == v:
                continue
            
            # Verifica se a aresta já existe
            exists = False
            for e in self.edges:
                if e['u'] == u and e['v'] == v:
                    exists = True
                    break
            
            if not exists:
                w = round(random.uniform(0.5, 5.0), 1)
                self.edges.append({'u': u, 'v': v, 'w': w})
                if not self.directed:
                    self.edges.append({'u': v, 'v': u, 'w': w})
        
        if self.sidebar:
            self.sidebar.update_vertices(sorted(list(self.nodes.keys())))
        
        if self.graph_editor:
            self.graph_editor.redraw_all()

    def clear_all(self):
        """Limpa todo o grafo."""
        self.nodes.clear()
        self.edges.clear()
        self.node_art.clear()
        self.edge_art.clear()
        self.next_node_id = 1
        self.last_dist.clear()
        self.last_prev.clear()
        self.last_source = None
        self.selected_for_edge = None
        self.dragging_node = None
        
        if self.sidebar:
            self.sidebar.update_vertices([])
            self.sidebar.clear_output()
        
        if self.graph_editor:
            self.graph_editor.redraw_all()

    def run_dijkstra(self):
        """Executa o algoritmo de Dijkstra."""
        if not self.sidebar or not self.sidebar.source_var:
            return
        
        source_label = self.sidebar.source_var.get()
        
        if not source_label or source_label not in self.nodes:
            alert_box = Tk()
            alert_box.iconbitmap('assets/icon.ico')
            alert_box.resizable(False, False)
            alert_box.geometry('320x180')
            alert_box.title('DijkstraLab')

            container = Frame(alert_box, bg=LIGHT_TURQUOISE)
            container.pack(fill='both', expand=True)

            label = Label(container, font=FONT_FAMILY, text='Selecione um vértice válido como origem.', bg=LIGHT_TURQUOISE, fg=LIGHT_GRAY)
            label.grid(row=0, column=0, padx=25, pady=35)

            def close_alert():
                alert_box.destroy()

            button = Button(container, text='Ok', bd=0, font=FONT_FAMILY, fg=LIGHT_GRAY, activeforeground=LIGHT_GRAY, bg=DARK_TURQUOISE, activebackground=DARK_TURQUOISE, command=close_alert)
            button.grid(row=1, column=0, padx=50, ipadx=15, ipady=7)

            alert_box.mainloop()
            return

        # Constrói lista de adjacência
        adj = {lbl: [] for lbl in self.nodes.keys()}
        for e in self.edges:
            adj[e['u']].append((e['v'], float(e['w'])))

        # Executa Dijkstra
        dist, prev = dijkstra(adj, source_label)
        
        # Armazena resultado
        self.last_dist = dist
        self.last_prev = prev
        self.last_source = source_label

        # Mostra resultado
        if self.sidebar:
            graph_type = 'Não Direcionado' if not self.directed else 'Direcionado'
            out_lines = [f"Dijkstra - Origem: {source_label} ({graph_type})\n"]
            out_lines.append("=" * 40 + "\n\n")
            
            for v in sorted(adj.keys()):
                d = dist.get(v, float('inf'))
                if d == float('inf'):
                    out_lines.append(f"{v}: ∞ (inalcançável)\n")
                else:
                    # Reconstrói caminho
                    path = []
                    cur = v
                    while cur is not None:
                        path.append(cur)
                        cur = prev.get(cur)
                    path = list(reversed(path))
                    
                    out_lines.append(f"{v}: {d:.1f}\n")
                    out_lines.append(f"  Caminho: {' → '.join(path)}\n\n")
            
            text = ''.join(out_lines)
            self.sidebar.output_text.config(state='normal')
            self.sidebar.output_text.delete('1.0', END)
            self.sidebar.output_text.insert(END, text)
            self.sidebar.output_text.config(state='disabled')
        
        # Redesenha para destacar o nó origem e arestas do caminho
        if self.graph_editor:
            self.graph_editor.redraw_all()

    def start(self):
        # Cria os componentes passando a referência do app
        self.top_menu = TopMenu(self)
        self.top_menu.start()

        self.graph_editor = GraphEditor(self)
        self.graph_editor.start()

        self.sidebar = Sidebar(self)
        self.sidebar.start(self.directed, sorted(list(self.nodes.keys())))

        self.mainloop()