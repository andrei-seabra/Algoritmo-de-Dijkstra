from ui_builder import TopMenu, GraphEditor, Sidebar
from tkinter import *
from tkinter import messagebox
from utils import dijkstra

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
        """Gera um grafo de exemplo."""
        self.clear_all()
        
        # Cria grafo de exemplo
        coords = [(150, 150), (350, 120), (550, 180), (400, 320), (200, 300)]
        labels = []
        for (x, y) in coords:
            # Gera label manualmente
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
        
        # Cria arestas
        if len(labels) >= 5:
            edge_list = [
                (labels[0], labels[1], 2.0),
                (labels[1], labels[2], 1.5),
                (labels[2], labels[3], 2.2),
                (labels[0], labels[4], 3.1),
                (labels[4], labels[3], 1.0)
            ]
            
            for u, v, w in edge_list:
                self.edges.append({'u': u, 'v': v, 'w': w})
                # Se não for direcionado, adiciona aresta reversa
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
            messagebox.showinfo('Dijkstra', 'Selecione um vértice válido como origem.')
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