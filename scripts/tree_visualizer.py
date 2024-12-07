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
            # Create node label from available information
            label_parts = []
            if member.get('name'):
                label_parts.append(member['name'])
            if member.get('age'):
                label_parts.append(f"Age: {member['age']}")
            if member.get('occupation'):
                label_parts.append(member['occupation'])
                
            label = '\n'.join(label_parts) if label_parts else f"Member {member_id}"
            
            # Add node with member information
            G.add_node(member_id, 
                      label=label,
                      gender=member.get('gender', 'other'),
                      age=member.get('age'),
                      member_data=member)
        
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
            member_data = G.nodes[node]['member_data']
            labels[node] = G.nodes[node]['label']
            
            # Color by gender
            gender = member_data.get('gender', 'other').lower()
            if gender == 'male':
                node_colors.append('lightblue')
            elif gender == 'female':
                node_colors.append('pink')
            elif gender == 'alien':
                node_colors.append('lightgreen')
            else:
                node_colors.append('lightgray')
            
            # Size nodes based on age if available, otherwise use default size
            if member_data.get('age'):
                # Scale age to a reasonable node size (e.g., 300-1000)
                node_sizes.append(300 + min(member_data['age'] * 10, 700))
            else:
                node_sizes.append(500)
        
        # Layout for the graph
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Draw the graph
        nx.draw_networkx_nodes(G, pos, 
                             node_color=node_colors, 
                             node_size=node_sizes, 
                             alpha=0.8, 
                             ax=ax)
        
        # Draw edges with different styles for different relationships
        # Parent relationships
        parent_edges = [(u, v) for (u, v, d) in G.edges(data=True) 
                       if d['relationship'] == 'parent']
        nx.draw_networkx_edges(G, pos, 
                             edgelist=parent_edges,
                             edge_color='green',
                             arrows=True,
                             arrowsize=20,
                             ax=ax)
        
        # Spouse relationships
        spouse_edges = [(u, v) for (u, v, d) in G.edges(data=True) 
                       if d['relationship'] == 'spouse']
        nx.draw_networkx_edges(G, pos, 
                             edgelist=spouse_edges,
                             edge_color='red',
                             style='dashed',
                             arrows=False,
                             ax=ax)
        
        # Add labels with smaller font size and word wrap
        label_pos = pos.copy()
        for node, (x, y) in pos.items():
            label_pos[node] = (x, y + 0.08)  # Adjust label position slightly above node
            
        nx.draw_networkx_labels(G, label_pos, labels, 
                              font_size=8,
                              bbox=dict(facecolor='white', 
                                      edgecolor='none', 
                                      alpha=0.7),
                              ax=ax)
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], color='green', label='Parent'),
            plt.Line2D([0], [0], color='red', linestyle='--', label='Spouse'),
            plt.scatter([0], [0], color='lightblue', label='Male'),
            plt.scatter([0], [0], color='pink', label='Female'),
            plt.scatter([0], [0], color='lightgreen', label='Alien'),
            plt.scatter([0], [0], color='lightgray', label='Other')
        ]
        ax.legend(handles=legend_elements, loc='upper left', 
                 bbox_to_anchor=(1, 1))
        
        # Remove axis
        ax.set_title("Family Tree Visualization")
        ax.set_axis_off()
        
        # Adjust layout to make room for the legend
        plt.subplots_adjust(right=0.85)
        
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
        self.viz_window.destroy()
        self.__init__(self.family_tree)
    
    def _save_visualization(self):
        """
        Save the current visualization as an image
        """
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filename:
            plt.savefig(filename, bbox_inches='tight', dpi=300)
            messagebox.showinfo("Success", f"Visualization saved to {filename}")

# Function to integrate with FamilyTreeUI
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