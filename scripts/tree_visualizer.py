import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FamilyTreeVisualization:
    def __init__(self, family_tree):
        """
        Initialize Family Tree Visualization
        
        :param family_tree: FamilyTree instance to visualize
        """
        self.family_tree = family_tree
        
        # Create visualization window
        self.viz_window = tk.Toplevel()
        self.viz_window.title("Family Tree Visualization")
        self.viz_window.geometry("800x600")
        
        # Create graph visualization
        self._create_graph_visualization()
        
    def _create_graph_visualization(self):
        """
        Create a networkx graph representation of the family tree
        """
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes (family members)
        for member_id, member in self.family_tree.members.items():
            # Add node with member information
            G.add_node(member_id, 
                name=member['name'], 
                birth_date=member['birth_date'],
                gender=member['gender']
            )
        
        # Add edges (relationships)
        for member_id, relationships in self.family_tree.relationships.items():
            for rel in relationships:
                if rel['relationship_type'] in ['parent', 'spouse']:
                    G.add_edge(member_id, rel['person_id'], 
                               relationship=rel['relationship_type'])
        
        # Create matplotlib figure
        plt.close('all')  # Close any existing plots
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Custom node coloring and sizing
        node_colors = []
        node_sizes = []
        labels = {}
        
        for node in G.nodes():
            member = self.family_tree.get_member(node)
            labels[node] = member['name']
            
            # Color by gender
            if member['gender'].lower() == 'male':
                node_colors.append('lightblue')
            elif member['gender'].lower() == 'female':
                node_colors.append('pink')
            else:
                node_colors.append('lightgray')
            
            # Size nodes based on number of relationships
            node_sizes.append(500 + 100 * len(list(G.predecessors(node))))
        
        # Layout for the graph
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        
        # Draw the graph
        nx.draw_networkx_nodes(G, pos, 
                                node_color=node_colors, 
                                node_size=node_sizes, 
                                alpha=0.8, 
                                ax=ax)
        
        # Draw edges with different styles
        for (u, v, data) in G.edges(data=True):
            if data.get('relationship') == 'spouse':
                nx.draw_networkx_edges(G, pos, 
                                       edgelist=[(u,v)], 
                                       edge_color='gray', 
                                       style='dashed', 
                                       ax=ax)
            else:
                nx.draw_networkx_edges(G, pos, 
                                       edgelist=[(u,v)], 
                                       edge_color='green', 
                                       arrows=True, 
                                       ax=ax)
        
        # Add labels
        nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax)
        
        # Remove axis
        ax.set_title("Family Tree Visualization")
        ax.set_axis_off()
        
        # Embed matplotlib figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.viz_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add interaction buttons
        button_frame = ttk.Frame(self.viz_window)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Regenerate layout button
        ttk.Button(button_frame, text="Regenerate Layout", 
                   command=self._regenerate_layout).pack(side=tk.LEFT, padx=5)
        
        # Save visualization button
        ttk.Button(button_frame, text="Save Visualization", 
                   command=self._save_visualization).pack(side=tk.LEFT, padx=5)
        
    def _regenerate_layout(self):
        """
        Regenerate the graph layout
        """
        # Close the current window and create a new visualization
        self.viz_window.destroy()
        self.__init__(self.family_tree)
    
    def _save_visualization(self):
        """
        Save the current visualization as an image
        """
        from tkinter import filedialog
        
        # Open file dialog to choose save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filename:
            plt.savefig(filename, bbox_inches='tight', dpi=300)
            messagebox.showinfo("Success", f"Visualization saved to {filename}")

# Integration with previous Family Tree UI
def add_visualization_to_ui(family_tree_ui):
    """
    Add a 'Visualize' button to the existing Family Tree UI
    
    :param family_tree_ui: The existing FamilyTreeUI instance
    """
    def open_visualization():
        FamilyTreeVisualization(family_tree_ui.family_tree)
    
    # Add Visualize button to the buttons frame
    ttk.Button(family_tree_ui.buttons_frame, text="Visualize Tree", 
               command=open_visualization).pack(side=tk.LEFT, padx=5)