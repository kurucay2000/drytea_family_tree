import tkinter as tk
from tkinter import ttk, messagebox
import graphviz


class FamilyTreeVisualization:
    def __init__(self, family_tree):
        self.family_tree = family_tree
        self._create_visualization()

    def _create_visualization(self):
        # Create a new directed graph
        dot = graphviz.Digraph(comment="Family Tree")
        dot.attr(rankdir="TB")  # Top to bottom direction

        # Add all members as nodes
        for name, member in self.family_tree.members.items():
            # Create label with name and age if available
            label_parts = [name]
            if member.get("age"):
                label_parts.append(f"Age: {member['age']}")

            # Set node color based on gender
            color = "lightgray"  # default color
            if member.get("gender"):
                if member["gender"].lower() == "female":
                    color = "pink"
                elif member["gender"].lower() == "male":
                    color = "lightblue"

            # Add node
            dot.node(
                name,  # Use name as node identifier
                "\n".join(label_parts),
                style="filled",
                fillcolor=color,
                shape="box",
            )

        # Add parent-child relationships
        for name, member in self.family_tree.members.items():
            # Handle father relationship
            if member.get("father"):
                dot.edge(member["father"], name)

            # Handle mother relationship
            if member.get("mother"):
                dot.edge(member["mother"], name)

        # Render the graph
        try:
            dot.render("family_tree", view=True, cleanup=True)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to create visualization: {str(e)}\n\nPlease make sure Graphviz is installed on your system.",
            )


def add_visualization_to_ui(family_tree_ui):
    def show_visualization():
        FamilyTreeVisualization(family_tree_ui.family_tree)

    ttk.Button(
        family_tree_ui.buttons_frame,
        text="Show Family Tree",
        command=show_visualization,
    ).pack(side=tk.LEFT, padx=5)
