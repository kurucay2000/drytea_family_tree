import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json

class FamilyTreeUI:
    def __init__(self, family_tree):
        """Initialize the Family Tree GUI"""
        self.family_tree = family_tree
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Family Tree Viewer")
        self.root.geometry("1000x700")  # Increased size for more details
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create UI components
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all UI widgets"""
        # Left side - Member List
        left_frame = ttk.Frame(self.main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Family Members", font=("Arial", 12, "bold")).pack()
        
        self.member_listbox = tk.Listbox(left_frame, width=30)
        self.member_listbox.pack(fill=tk.BOTH, expand=True)
        self.member_listbox.bind('<<ListboxSelect>>', self._on_member_select)
        
        self._populate_member_list()
        
        # Right side - Member Details
        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Details Frame
        details_frame = ttk.LabelFrame(right_frame, text="Member Details")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Details Labels and Variables
        self.detail_vars = {
            'name': tk.StringVar(),
            'age': tk.StringVar(),
            'gender': tk.StringVar(),
            'location': tk.StringVar(),
            'occupation': tk.StringVar(),
            'aspiration': tk.StringVar(),
            'cause_of_death': tk.StringVar(),
            'extra_information': tk.StringVar()
        }
        
        detail_labels = [
            ("Name:", 'name'),
            ("Age:", 'age'),
            ("Gender:", 'gender'),
            ("Location:", 'location'),
            ("Occupation:", 'occupation'),
            ("Aspiration:", 'aspiration'),
            ("Cause of Death:", 'cause_of_death'),
            ("Extra Information:", 'extra_information')
        ]
        
        for i, (label_text, var_key) in enumerate(detail_labels):
            ttk.Label(details_frame, text=label_text).grid(row=i, column=0, sticky='w', padx=5, pady=2)
            ttk.Label(details_frame, textvariable=self.detail_vars[var_key]).grid(row=i, column=1, sticky='w', padx=5, pady=2)
        
        # Relationships Frame
        relationships_frame = ttk.LabelFrame(right_frame, text="Relationships")
        relationships_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.relationships_listbox = tk.Listbox(relationships_frame)
        self.relationships_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        self.buttons_frame = buttons_frame
        
        ttk.Button(buttons_frame, text="Add Member", command=self._add_member).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Add Relationship", command=self._add_relationship).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Save Tree", command=self._save_tree).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Load Tree", command=self._load_tree).pack(side=tk.LEFT, padx=5)
    
    def _add_member(self):
        """Open dialog to add a new family member"""
        fields = [
            ("Name", str, None),
            ("Age", int, None),
            ("Gender", str, ["Male", "Female", "Alien", "Other"]),
            ("Location", str, None),
            ("Occupation", str, None),
            ("Aspiration", str, None),
            ("Cause of Death", str, None),
            ("Extra Information", str, None)
        ]
        
        values = {}
        for field_name, field_type, options in fields:
            if options:
                # Create a selection dialog for fields with options
                dialog = tk.Toplevel(self.root)
                dialog.title(f"Select {field_name}")
                dialog.geometry("200x200")
                
                selected_value = [None]
                
                for option in options:
                    def make_command(opt):
                        return lambda: (selected_value.__setitem__(0, opt), dialog.destroy())
                    
                    ttk.Button(dialog, text=option, 
                             command=make_command(option)).pack(pady=5)
                
                dialog.wait_window()
                value = selected_value[0]
            else:
                # Use simple dialog for other fields
                value = simpledialog.askstring("Add Member", f"Enter {field_name}:")
            
            if value:
                try:
                    if field_type == int and value:
                        # Convert to float first to handle decimal inputs, then to int
                        value = int(float(value))
                        if value < 0:
                            raise ValueError("Age cannot be negative")
                    values[field_name.lower().replace(" ", "_")] = field_type(value)
                except ValueError as e:
                    if str(e) == "Age cannot be negative":
                        messagebox.showerror("Error", "Age cannot be negative")
                    else:
                        messagebox.showerror("Error", f"Invalid value for {field_name}. Must be a whole number.")
                    return
        
        # Add member to family tree
        try:
            member_id = self.family_tree.add_member(**values)
            self._populate_member_list()
            messagebox.showinfo("Success", f"Added {values.get('name', 'new member')} to the family tree!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _add_relationship(self):
        """Open dialog to add a relationship between two members"""
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
        try:
            self.family_tree.add_relationship(
                first_member['id'], 
                second_member['id'], 
                relationship_type
            )
            
            messagebox.showinfo("Success", 
                f"Added {relationship_type} relationship between "
                f"{first_member.get('name', 'Member ' + str(first_member['id']))} and "
                f"{second_member.get('name', 'Member ' + str(second_member['id']))}")
            
            # Refresh current member view if applicable
            selections = self.member_listbox.curselection()
            if selections:
                self._on_member_select(None)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _select_member(self, title, exclude=None):
        """Open a dialog to select a family member"""
        select_dialog = tk.Toplevel(self.root)
        select_dialog.title(title)
        select_dialog.geometry("300x400")
        
        selected_member = [None]
        
        member_select_listbox = tk.Listbox(select_dialog)
        member_select_listbox.pack(fill=tk.BOTH, expand=True)
        
        for member_id, member in self.family_tree.members.items():
            if exclude is None or member_id != exclude:
                name = member.get('name', f"Member {member_id}")
                member_select_listbox.insert(tk.END, f"{name} (ID: {member_id})")
        
        def on_select():
            if member_select_listbox.curselection():
                selection = member_select_listbox.get(member_select_listbox.curselection())
                member_id = int(selection.split('(ID: ')[1].strip(')'))
                selected_member[0] = self.family_tree.get_member(member_id)
                select_dialog.destroy()
        
        ttk.Button(select_dialog, text="Select", command=on_select).pack()
        
        select_dialog.wait_window()
        return selected_member[0]
    
    def _save_tree(self):
        """Save the family tree to a JSON file"""
        save_data = {
            'members': self.family_tree.members,
            'relationships': self.family_tree.relationships
        }
        
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(save_data, f, indent=4)
                messagebox.showinfo("Success", f"Family tree saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save family tree: {str(e)}")
    
    def _load_tree(self):
        """Load a family tree from a JSON file"""
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
    
    def _on_member_select(self, event):
        """Handle member selection in the listbox"""
        if not self.member_listbox.curselection():
            return
        
        selection = self.member_listbox.get(self.member_listbox.curselection())
        member_id = int(selection.split('(ID: ')[1].strip(')'))
        
        member = self.family_tree.get_member(member_id)
        
        # Update detail variables
        for key, var in self.detail_vars.items():
            value = member.get(key)
            var.set(str(value) if value is not None else "")
        
        # Update relationships
        self.relationships_listbox.delete(0, tk.END)
        relationships = self.family_tree.get_relationships(member_id)
        for rel in relationships:
            related_member = self.family_tree.get_member(rel['person_id'])
            name = related_member.get('name', f"Member {rel['person_id']}")
            self.relationships_listbox.insert(tk.END, 
                f"{rel['relationship_type']}: {name}")
    
    def _populate_member_list(self):
        """Populate the member listbox with names from the family tree"""
        self.member_listbox.delete(0, tk.END)
        for member_id, member in self.family_tree.members.items():
            name = member.get('name', f"Member {member_id}")
            self.member_listbox.insert(tk.END, f"{name} (ID: {member_id})")
    
    def run(self):
        """Start the Tkinter event loop"""
        self.root.mainloop()