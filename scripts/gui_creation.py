import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json

class FamilyTreeUI:
    def __init__(self, family_tree):
        """
        Initialize the Family Tree GUI
        
        :param family_tree: FamilyTree instance to display and manipulate
        """
        self.family_tree = family_tree
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Family Tree Viewer")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create UI components
        self._create_widgets()
        
    def _create_widgets(self):
        """
        Create and layout all UI widgets
        """
        # Left side - Member List
        left_frame = ttk.Frame(self.main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Member List Label
        ttk.Label(left_frame, text="Family Members", font=("Arial", 12, "bold")).pack()
        
        # Member Listbox
        self.member_listbox = tk.Listbox(left_frame, width=30)
        self.member_listbox.pack(fill=tk.BOTH, expand=True)
        self.member_listbox.bind('<<ListboxSelect>>', self._on_member_select)
        
        # Populate Member List
        self._populate_member_list()
        
        # Right side - Member Details
        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Details Frame
        details_frame = ttk.LabelFrame(right_frame, text="Member Details")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Details Labels
        self.detail_vars = {
            'name': tk.StringVar(),
            'birth_date': tk.StringVar(),
            'gender': tk.StringVar(),
        }
        
        detail_labels = [
            ("Name:", 'name'),
            ("Birth Date:", 'birth_date'),
            ("Gender:", 'gender')
        ]
        
        for i, (label_text, var_key) in enumerate(detail_labels):
            ttk.Label(details_frame, text=label_text).grid(row=i, column=0, sticky='w', padx=5, pady=2)
            ttk.Label(details_frame, textvariable=self.detail_vars[var_key]).grid(row=i, column=1, sticky='w', padx=5, pady=2)
        
        # Additional Info Text Widget
        ttk.Label(details_frame, text="Additional Info:").grid(row=len(detail_labels), column=0, columnspan=2, sticky='w', padx=5, pady=2)
        self.additional_info_text = tk.Text(details_frame, height=5, width=40, state='disabled')
        self.additional_info_text.grid(row=len(detail_labels)+1, column=0, columnspan=2, padx=5, pady=2)
        
        # Relationships Frame
        relationships_frame = ttk.LabelFrame(right_frame, text="Relationships")
        relationships_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Relationships Listbox
        self.relationships_listbox = tk.Listbox(relationships_frame, width=40)
        self.relationships_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        # Add Member Button
        ttk.Button(buttons_frame, text="Add Member", command=self._add_member).pack(side=tk.LEFT, padx=5)
        
        # Add Relationship Button
        ttk.Button(buttons_frame, text="Add Relationship", command=self._add_relationship).pack(side=tk.LEFT, padx=5)
        
        # Save and Load Buttons
        ttk.Button(buttons_frame, text="Save Tree", command=self._save_tree).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Load Tree", command=self._load_tree).pack(side=tk.LEFT, padx=5)
        
    def _populate_member_list(self):
        """
        Populate the member listbox with names from the family tree
        """
        self.member_listbox.delete(0, tk.END)
        for member_id, member in self.family_tree.members.items():
            self.member_listbox.insert(tk.END, f"{member['name']} (ID: {member_id})")
        
    def _on_member_select(self, event):
        """
        Handle member selection in the listbox
        """
        # Get selected member
        if not self.member_listbox.curselection():
            return
        
        selection = self.member_listbox.get(self.member_listbox.curselection())
        member_id = int(selection.split('(ID: ')[1].strip(')'))
        
        # Get member details
        member = self.family_tree.get_member(member_id)
        
        # Update detail variables
        self.detail_vars['name'].set(member['name'])
        self.detail_vars['birth_date'].set(member['birth_date'])
        self.detail_vars['gender'].set(member['gender'])
        
        # Update additional info
        self.additional_info_text.config(state='normal')
        self.additional_info_text.delete(1.0, tk.END)
        if member['additional_info']:
            for key, value in member['additional_info'].items():
                self.additional_info_text.insert(tk.END, f"{key}: {value}\n")
        self.additional_info_text.config(state='disabled')
        
        # Update relationships
        self.relationships_listbox.delete(0, tk.END)
        relationships = self.family_tree.get_relationships(member_id)
        for rel in relationships:
            related_member = self.family_tree.get_member(rel['person_id'])
            self.relationships_listbox.insert(tk.END, 
                f"{rel['relationship_type']}: {related_member['name']}")
        
    def _add_member(self):
        """
        Open dialog to add a new family member
        """
        # Name input
        name = simpledialog.askstring("Add Member", "Enter Name:")
        if not name:
            return
        
        # Birth Date input
        birth_date = simpledialog.askstring("Add Member", "Enter Birth Date (YYYY-MM-DD):")
        if not birth_date:
            return
        
        # Gender input
        gender = simpledialog.askstring("Add Member", "Enter Gender:")
        if not gender:
            return
        
        # Additional info (optional)
        additional_info = {}
        while True:
            key = simpledialog.askstring("Additional Info", 
                "Enter info key (or leave blank to finish):")
            if not key:
                break
            value = simpledialog.askstring("Additional Info", 
                f"Enter value for {key}:")
            if value:
                additional_info[key] = value
        
        # Add member to family tree
        member_id = self.family_tree.add_member(
            name, birth_date, gender, additional_info
        )
        
        # Refresh member list
        self._populate_member_list()
        
        messagebox.showinfo("Success", f"Added {name} to the family tree!")
        
    def _add_relationship(self):
        """
        Open dialog to add a relationship between two members
        """
        if len(self.family_tree.members) < 2:
            messagebox.showerror("Error", "You need at least two members to add a relationship!")
            return
        
        # Select first person
        first_member = self._select_member("Select First Person")
        if not first_member:
            return
        
        # Select second person
        second_member = self._select_member("Select Second Person", exclude=first_member['id'])
        if not second_member:
            return
        
        # Relationship type
        relationship_type = simpledialog.askstring("Add Relationship", 
            "Enter Relationship Type (e.g., parent, spouse, sibling):")
        if not relationship_type:
            return
        
        # Add relationship
        self.family_tree.add_relationship(
            first_member['id'], 
            second_member['id'], 
            relationship_type
        )
        
        messagebox.showinfo("Success", 
            f"Added {relationship_type} relationship between "
            f"{first_member['name']} and {second_member['name']}")
        
        # Refresh current member view if applicable
        selections = self.member_listbox.curselection()
        if selections:
            self._on_member_select(None)
        
    def _select_member(self, title, exclude=None):
        """
        Open a dialog to select a family member
        
        :param title: Dialog title
        :param exclude: Optional member ID to exclude from selection
        :return: Selected member dictionary or None
        """
        # Create selection dialog
        select_dialog = tk.Toplevel(self.root)
        select_dialog.title(title)
        select_dialog.geometry("300x400")
        
        selected_member = [None]  # Mutable container for selected member
        
        # Listbox for member selection
        member_select_listbox = tk.Listbox(select_dialog)
        member_select_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Populate listbox
        for member_id, member in self.family_tree.members.items():
            if exclude is None or member_id != exclude:
                member_select_listbox.insert(tk.END, f"{member['name']} (ID: {member_id})")
        
        def on_select():
            """Internal function to handle selection"""
            if member_select_listbox.curselection():
                selection = member_select_listbox.get(member_select_listbox.curselection())
                member_id = int(selection.split('(ID: ')[1].strip(')'))
                selected_member[0] = self.family_tree.get_member(member_id)
                select_dialog.destroy()
        
        # Select button
        ttk.Button(select_dialog, text="Select", command=on_select).pack()
        
        # Wait for dialog to close
        select_dialog.wait_window()
        
        return selected_member[0]
    
    def _save_tree(self):
        """
        Save the family tree to a JSON file
        """
        # Convert family tree to a saveable format
        save_data = {
            'members': self.family_tree.members,
            'relationships': self.family_tree.relationships
        }
        
        # Use tkinter's file dialog to get save location
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=4)
            messagebox.showinfo("Success", f"Family tree saved to {filename}")
    
    def _load_tree(self):
        """
        Load a family tree from a JSON file
        """
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    load_data = json.load(f)
                
                # Clear existing tree
                self.family_tree.members = load_data['members']
                self.family_tree.relationships = load_data['relationships']
                
                # Refresh UI
                self._populate_member_list()
                messagebox.showinfo("Success", f"Family tree loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load family tree: {str(e)}")
    
    def run(self):
        """
        Start the Tkinter event loop
        """
        self.root.mainloop()
