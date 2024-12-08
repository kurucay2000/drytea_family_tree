import tkinter as tk
from tkinter import ttk, messagebox
import json


class AddMemberDialog:
    def __init__(self, parent, family_tree, callback):
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Family Member")
        self.dialog.geometry("500x700")

        # Store references
        self.family_tree = family_tree
        self.callback = callback

        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Create main frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add title
        ttk.Label(
            main_frame, text="Add New Family Member", font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))

        # Create details frame
        details_frame = ttk.LabelFrame(main_frame, text="Member Details")
        details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create and store detail variables
        self.detail_vars = {
            "id": tk.StringVar(),
            "name": tk.StringVar(),
            "age": tk.StringVar(),
            "gender": tk.StringVar(),
            "location": tk.StringVar(),
            "occupation": tk.StringVar(),
            "aspiration": tk.StringVar(),
            "cause_of_death": tk.StringVar(),
            "father": tk.StringVar(),
            "mother": tk.StringVar(),
        }

        # Regular fields
        regular_fields = [
            ("ID:", "id"),
            ("Name:", "name"),
            ("Age:", "age"),
            ("Gender:", "gender"),
            ("Location:", "location"),
            ("Occupation:", "occupation"),
            ("Aspiration:", "aspiration"),
            ("Cause of Death:", "cause_of_death"),
            ("Father:", "father"),
            ("Mother:", "mother"),
        ]

        # Create entry fields
        self.detail_entries = {}

        for i, (label_text, var_key) in enumerate(regular_fields):
            ttk.Label(details_frame, text=label_text).grid(
                row=i, column=0, sticky="w", padx=5, pady=2
            )

            if var_key == "gender":
                self.detail_entries[var_key] = ttk.Combobox(
                    details_frame,
                    textvariable=self.detail_vars[var_key],
                    values=["Male", "Female", "Alien", "Other"],
                )
            elif var_key == "id":
                self.detail_entries[var_key] = ttk.Entry(
                    details_frame,
                    textvariable=self.detail_vars[var_key],
                    state="readonly",
                )
            else:
                self.detail_entries[var_key] = ttk.Entry(
                    details_frame, textvariable=self.detail_vars[var_key]
                )

            self.detail_entries[var_key].grid(
                row=i, column=1, sticky="ew", padx=5, pady=2
            )

        # Set next available ID
        next_id = (
            max(
                [member.get("id", 0) for member in self.family_tree.members.values()],
                default=0,
            )
            + 1
        )
        self.detail_vars["id"].set(str(next_id))

        # Extra Information Text Area
        ttk.Label(details_frame, text="Extra Information:").grid(
            row=len(regular_fields), column=0, sticky="nw", padx=5, pady=2
        )

        # Create text frame for extra information
        text_frame = ttk.Frame(details_frame)
        text_frame.grid(
            row=len(regular_fields), column=1, sticky="nsew", padx=5, pady=2
        )

        self.extra_info_text = tk.Text(text_frame, wrap=tk.WORD, height=8, width=40)
        scrollbar = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.extra_info_text.yview
        )

        self.extra_info_text.configure(yscrollcommand=scrollbar.set)
        self.extra_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure grid weights for details frame
        details_frame.grid_columnconfigure(1, weight=1)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(
            side=tk.RIGHT, padx=5
        )
        ttk.Button(button_frame, text="Add Member", command=self._add_member).pack(
            side=tk.RIGHT, padx=5
        )

    def _add_member(self):
        """Process the form data and add the member"""
        values = {}

        # Get values from entry fields
        for field_name, var in self.detail_vars.items():
            value = var.get().strip()
            if value:  # Only include non-empty values
                if field_name == "age":
                    try:
                        value = int(float(value))
                        if value < 0:
                            messagebox.showerror("Error", "Age cannot be negative")
                            return
                    except ValueError:
                        messagebox.showerror("Error", "Age must be a valid number")
                        return
                values[field_name] = value

        # Get extra information
        extra_info = self.extra_info_text.get("1.0", tk.END).strip()
        if extra_info:
            values["extra_information"] = extra_info

        try:
            # Add member to family tree
            self.family_tree.add_member(**values)

            # Update members.json
            members_data = []
            for member_id, member in self.family_tree.members.items():
                member_data = member.copy()
                member_data["id"] = member.get("id")  # Ensure ID is included
                members_data.append(member_data)

            with open("./data/members.json", "w") as f:
                json.dump(members_data, f, indent=4)

            # Call callback to refresh member list
            self.callback()

            messagebox.showinfo(
                "Success",
                f"Added {values.get('name', 'new member')} to the family tree!",
            )
            self.dialog.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))


class FamilyTreeUI:
    def __init__(self, family_tree):
        """Initialize the Family Tree GUI"""
        self.family_tree = family_tree

        # Create main window
        self.root = tk.Tk()
        self.root.title("Family Tree Viewer")
        self.root.geometry("1000x800")

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Store currently selected member ID
        self.current_member_id = None

        # Initialize member_ids list
        self.member_ids = []

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
        self.member_listbox.bind("<<ListboxSelect>>", self._on_member_select)

        self._populate_member_list()

        # Right side - Member Details
        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Details Frame
        details_frame = ttk.LabelFrame(right_frame, text="Member Details")
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Details Entry Fields and Variables
        self.detail_vars = {
            "id": tk.StringVar(),
            "name": tk.StringVar(),
            "age": tk.StringVar(),
            "gender": tk.StringVar(),
            "location": tk.StringVar(),
            "occupation": tk.StringVar(),
            "aspiration": tk.StringVar(),
            "cause_of_death": tk.StringVar(),
            "father": tk.StringVar(),
            "mother": tk.StringVar(),
        }

        # Store entry widgets
        self.detail_entries = {}

        # Regular fields
        regular_fields = [
            ("ID:", "id"),
            ("Name:", "name"),
            ("Age:", "age"),
            ("Gender:", "gender"),
            ("Location:", "location"),
            ("Occupation:", "occupation"),
            ("Aspiration:", "aspiration"),
            ("Cause of Death:", "cause_of_death"),
            ("Father:", "father"),
            ("Mother:", "mother"),
        ]

        for i, (label_text, var_key) in enumerate(regular_fields):
            ttk.Label(details_frame, text=label_text).grid(
                row=i, column=0, sticky="w", padx=5, pady=2
            )

            if var_key == "gender":
                self.detail_entries[var_key] = ttk.Combobox(
                    details_frame,
                    textvariable=self.detail_vars[var_key],
                    values=["Male", "Female", "Alien", "Other"],
                )
            elif var_key == "id":
                self.detail_entries[var_key] = ttk.Entry(
                    details_frame,
                    textvariable=self.detail_vars[var_key],
                    state="readonly",
                )
            else:
                self.detail_entries[var_key] = ttk.Entry(
                    details_frame, textvariable=self.detail_vars[var_key]
                )

            self.detail_entries[var_key].grid(
                row=i, column=1, sticky="ew", padx=5, pady=2
            )

        # Extra Information Text Area
        ttk.Label(details_frame, text="Extra Information:").grid(
            row=len(regular_fields), column=0, sticky="nw", padx=5, pady=2
        )

        # Create a frame for the text area and scrollbar
        text_frame = ttk.Frame(details_frame)
        text_frame.grid(
            row=len(regular_fields), column=1, sticky="nsew", padx=5, pady=2
        )

        # Create text widget and scrollbar separately for more control
        self.extra_info_text = tk.Text(text_frame, wrap=tk.WORD, height=8, width=40)
        scrollbar = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.extra_info_text.yview
        )

        # Configure text widget to use scrollbar
        self.extra_info_text.configure(yscrollcommand=self._on_scroll)

        # Pack the text widget and scrollbar
        self.extra_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Save Changes Button
        self.save_changes_btn = ttk.Button(
            details_frame, text="Save Changes", command=self._save_member_changes
        )
        self.save_changes_btn.grid(
            row=len(regular_fields) + 1, column=0, columnspan=2, pady=10
        )
        self.save_changes_btn.grid_remove()  # Hide initially

        # Buttons Frame
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        self.buttons_frame = buttons_frame

        ttk.Button(buttons_frame, text="Add Member", command=self._add_member).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(
            buttons_frame, text="Remove Member", command=self._remove_member
        ).pack(side=tk.LEFT, padx=5)

    def _populate_member_list(self):
        """Populate the member listbox with names from the family tree"""
        # Store current selection
        current_selection = self.member_listbox.curselection()

        # Clear the listbox
        self.member_listbox.delete(0, tk.END)

        # Create a list to store member IDs in parallel with listbox entries
        self.member_ids = []

        # Sort members by ID
        sorted_members = sorted(
            self.family_tree.members.items(), key=lambda x: x[1].get("id", float("inf"))
        )

        for member_id, member in sorted_members:
            name = member.get("name", "Unknown")
            # Add only the name to the listbox
            self.member_listbox.insert(tk.END, name)
            # Store the ID in our parallel list
            self.member_ids.append(member_id)

        # Restore selection if possible
        if current_selection:
            self.member_listbox.selection_set(current_selection)

    def _on_member_select(self, event):
        """Handle member selection in the listbox"""
        if not self.member_listbox.curselection():
            return

        try:
            # Get the selected index
            selection_index = self.member_listbox.curselection()[0]
            # Get the member name from our parallel list (since we use names as keys)
            member_name = self.member_ids[selection_index]

            # Get the member data
            member = self.family_tree.members[member_name]

            # Update detail variables
            for key, var in self.detail_vars.items():
                if key == "id":
                    # Try to get ID - we know it exists in the member data
                    id_value = member.get("id", "ID Missing")
                    var.set(str(id_value))
                else:
                    value = member.get(key)
                    var.set(str(value) if value is not None else "")

            # Update extra information text area
            self.extra_info_text.delete("1.0", tk.END)
            if member.get("extra_information"):
                self.extra_info_text.insert("1.0", member["extra_information"])

            # Show the save changes button
            self.save_changes_btn.grid()

            # Update father and mother fields with names
            for key in ["father", "mother"]:
                value = member.get(key)
                if value:
                    parent = self.family_tree.members.get(value)
                    self.detail_vars[key].set(parent["name"] if parent else "")
                else:
                    self.detail_vars[key].set("")

        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while loading member details: {str(e)}"
            )

    def _save_member_changes(self):
        """Save changes made to member details with confirmation dialog"""
        if self.current_member_id is None:
            return

        try:
            # Get current member data
            member = self.family_tree.members[self.current_member_id]

            # Get all values from entry fields
            updated_values = {}
            changes_description = []

            # Handle regular fields
            for key, var in self.detail_vars.items():
                new_value = var.get().strip()
                old_value = (
                    str(member.get(key, "")) if member.get(key) is not None else ""
                )

                if new_value != old_value:  # Only track changed values
                    if key == "age" and new_value:
                        try:
                            new_value = int(float(new_value))
                            if new_value < 0:
                                raise ValueError("Age cannot be negative")
                        except ValueError as e:
                            if str(e) == "Age cannot be negative":
                                messagebox.showerror("Error", "Age cannot be negative")
                            else:
                                messagebox.showerror(
                                    "Error", "Age must be a valid number"
                                )
                            return

                    if new_value:  # Only include non-empty values
                        updated_values[key] = new_value
                        field_name = key.replace("_", " ").title()
                        if old_value:
                            changes_description.append(
                                f"{field_name}: '{old_value}' → '{new_value}'"
                            )
                        else:
                            changes_description.append(
                                f"{field_name}: Added '{new_value}'"
                            )

            # Handle extra information separately
            new_extra_info = self.extra_info_text.get("1.0", tk.END).strip()
            old_extra_info = member.get("extra_information", "")

            if new_extra_info != old_extra_info:
                updated_values["extra_information"] = new_extra_info
                if old_extra_info:
                    changes_description.append("Extra Information has been modified")
                else:
                    changes_description.append("Extra Information has been added")

            # If no changes were made, show message and return
            if not changes_description:
                messagebox.showinfo(
                    "No Changes", "No changes were made to the member details."
                )
                return

            # Create confirmation dialog
            confirm_message = "The following changes will be made:\n\n"
            confirm_message += "\n".join(changes_description)
            confirm_message += "\n\nDo you want to save these changes?"

            if messagebox.askyesno("Confirm Changes", confirm_message):
                # Update member in family tree
                member.update(updated_values)

                # Update members.json
                members_data = []
                for member_id, member in self.family_tree.members.items():
                    member_data = member.copy()
                    member_data["id"] = member.get("id")  # Ensure ID is included
                    members_data.append(member_data)

                with open("./data/members.json", "w") as f:
                    json.dump(members_data, f, indent=4)

                # Refresh the member list to show any name changes
                self._populate_member_list()
                messagebox.showinfo("Success", "Member details updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update member details: {str(e)}")

    def _remove_member(self):
        """Remove the currently selected member from the family tree and update JSON files"""
        if not self.current_member_id:
            messagebox.showinfo("No Selection", "Please select a member to remove.")
            return

        member = self.family_tree.members[self.current_member_id]
        member_name = member.get("name", f"Member {self.current_member_id}")

        # Confirm deletion
        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to remove {member_name} from the family tree?\n\n"
            "This will also remove all relationships associated with this member.",
        ):
            return

        try:
            # Remove member from parents' children lists
            for parent_key in ["father", "mother"]:
                parent_id = member.get(parent_key)
                if parent_id and parent_id in self.family_tree.members:
                    parent = self.family_tree.members[parent_id]
                    if (
                        "children" in parent
                        and self.current_member_id in parent["children"]
                    ):
                        parent["children"].remove(self.current_member_id)

            # Remove the member
            del self.family_tree.members[self.current_member_id]

            # Update members.json
            members_data = []
            for member_id, member in self.family_tree.members.items():
                member_data = member.copy()
                member_data["id"] = member.get("id")  # Ensure ID is included
                members_data.append(member_data)

            with open("./data/members.json", "w") as f:
                json.dump(members_data, f, indent=4)

            # Clear the details panel
            for var in self.detail_vars.values():
                var.set("")
            self.extra_info_text.delete("1.0", tk.END)
            self.save_changes_btn.grid_remove()

            # Reset current member ID
            self.current_member_id = None

            # Refresh the member list
            self._populate_member_list()

            messagebox.showinfo(
                "Success", f"{member_name} has been removed from the family tree."
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove member: {str(e)}")

    def _add_member(self):
        """Open dialog to add a new family member"""
        AddMemberDialog(self.root, self.family_tree, self._populate_member_list)

    def _on_scroll(self, *args):
        """Control scrollbar visibility based on content"""
        # Check if there's enough content to scroll
        if self.extra_info_text.yview() != (0.0, 1.0):
            # Content extends beyond visible area
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            # All content is visible
            self.scrollbar.pack_forget()
        # Update scrollbar position
        self.scrollbar.set(*args)

    def _get_member_id_by_name(self, name):
        """Helper function to get member ID by name"""
        for member_id, member in self.family_tree.members.items():
            if member.get("name") == name:
                return member_id
        return None

    def run(self):
        """Start the Tkinter event loop"""
        self.root.mainloop()
