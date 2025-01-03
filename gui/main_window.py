import tkinter as tk
from tkinter import ttk, messagebox
import json
from .add_member_dialog import AddMemberDialog
from .member_details_frame import MemberDetailsFrame


class FamilyTreeUI:
    def __init__(self, family_tree):
        self.family_tree = family_tree
        self.root = tk.Tk()
        self.root.title("Family Tree Viewer")
        self.root.geometry("1000x800")
        self.sort_by_last_name = True  # Default to sorting by last name

        # Set the theme colors
        self.root.configure(bg="#f0e6ff")  # Light purple background

        # Configure styles
        style = ttk.Style()
        style.configure("TFrame", background="#f0e6ff")
        style.configure("TLabelframe", background="#f0e6ff")
        style.configure("TLabelframe.Label", background="#f0e6ff", foreground="black")
        style.configure(
            "TButton",
            background="#6a0dad",  # Deep purple
            foreground="black",
            bordercolor="black",
            focuscolor="#8a2be2",
        )  # Lighter purple for focus
        style.configure("TLabel", background="#f0e6ff", foreground="black")
        style.configure("TEntry", fieldbackground="white", foreground="black")
        style.configure(
            "Treeview", background="white", fieldbackground="white", foreground="black"
        )
        style.configure(
            "TCombobox", fieldbackground="white", background="white", foreground="black"
        )

        self.main_frame = ttk.Frame(self.root, padding="10", style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.current_member_id = None
        self.member_ids = []
        self._create_widgets()

    # [Previous methods remain unchanged: _get_last_name, _get_first_name, _toggle_sort, _populate_member_list]
    def _get_last_name(self, member):
        """Extract last name from member data for sorting"""
        name = member.get("name", "Unknown")
        name_parts = name.strip().split()
        return name_parts[-1].lower() if name_parts else ""

    def _get_first_name(self, member):
        """Extract first name from member data for sorting"""
        name = member.get("name", "Unknown")
        name_parts = name.strip().split()
        return name_parts[0].lower() if name_parts else ""

    def _toggle_sort(self):
        """Toggle between first and last name sorting"""
        self.sort_by_last_name = not self.sort_by_last_name
        self._populate_member_list()
        # Update button text
        sort_text = (
            "Sort by First Name" if self.sort_by_last_name else "Sort by Last Name"
        )
        self.sort_button.configure(text=sort_text)

    def _populate_member_list(self):
        """Populate the member list sorted by chosen method"""
        current_selection = self.member_listbox.curselection()
        self.member_listbox.delete(0, tk.END)
        self.member_ids = []

        # Create list of members with their sorting information
        sorted_members = []
        for member_id, member in self.family_tree.members.items():
            if self.sort_by_last_name:
                sort_key = self._get_last_name(member)
            else:
                sort_key = self._get_first_name(member)
            full_name = member.get("name", "Unknown")
            sorted_members.append((sort_key, full_name, member_id))

        # Sort by chosen key, then by full name
        sorted_members.sort(key=lambda x: (x[0], x[1]))

        # Populate the listbox with sorted names
        for _, full_name, member_id in sorted_members:
            self.member_listbox.insert(tk.END, full_name)
            self.member_ids.append(member_id)

        if current_selection:
            self.member_listbox.selection_set(current_selection)

    def _create_widgets(self):
        # Left frame for member list and sorting controls
        left_frame = ttk.Frame(self.main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Title label for members list
        ttk.Label(left_frame, text="Family Members", font=("Arial", 12, "bold")).pack()

        # Member listbox with purple theme
        self.member_listbox = tk.Listbox(
            left_frame,
            width=30,
            bg="white",
            fg="black",
            selectbackground="#8a2be2",  # Purple selection
            selectforeground="white",
            font=("Arial", 10),
        )
        self.member_listbox.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar for member list
        list_scrollbar = ttk.Scrollbar(
            left_frame, orient=tk.VERTICAL, command=self.member_listbox.yview
        )
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.member_listbox.configure(yscrollcommand=list_scrollbar.set)

        # Add sort toggle button at the bottom
        self.sort_button = ttk.Button(
            left_frame,
            text="Sort by First Name",  # Initial text (since default is last name sort)
            command=self._toggle_sort,
            style="TButton",
        )
        self.sort_button.pack(side=tk.BOTTOM, pady=(5, 0))

        # Bind selection event
        self.member_listbox.bind("<<ListboxSelect>>", self._on_member_select)

        # Populate the member list
        self._populate_member_list()

        # Right frame for details and buttons
        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create member details frame
        self.details_frame = MemberDetailsFrame(
            right_frame, self.family_tree, self._save_member_changes
        )

        # Button frame
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        self.buttons_frame = (
            buttons_frame  # Store reference for adding visualization button
        )

        # Add Member button
        add_button = ttk.Button(
            buttons_frame, text="Add Member", command=self._add_member, style="TButton"
        )
        add_button.pack(side=tk.LEFT, padx=5)

        # Remove Member button
        remove_button = ttk.Button(
            buttons_frame,
            text="Remove Member",
            command=self._remove_member,
            style="TButton",
        )
        remove_button.pack(side=tk.LEFT, padx=5)

    def _on_member_select(self, event):
        if not self.member_listbox.curselection():
            return
        try:
            selection_index = self.member_listbox.curselection()[0]
            member_name = self.member_ids[selection_index]
            member = self.family_tree.members[member_name]
            self.details_frame.update_details(member)
            self.current_member_id = member_name
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while loading member details: {str(e)}"
            )

    def _save_member_changes(self, skip_save_check=False):
        """Save changes to member details"""
        if self.current_member_id is None:
            return

        # If skip_save_check is True, just refresh the member list
        if skip_save_check:
            self._populate_member_list()
            return

        try:
            member = self.family_tree.members[self.current_member_id]
            updated_values = {}
            changes_description = []
            for key, var in self.details_frame.detail_vars.items():
                new_value = var.get().strip()
                old_value = (
                    str(member.get(key, "")) if member.get(key) is not None else ""
                )
                if new_value != old_value:
                    if new_value:
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

            new_extra_info = self.details_frame.extra_info_text.get(
                "1.0", tk.END
            ).strip()
            old_extra_info = member.get("extra_information", "")
            if new_extra_info != old_extra_info:
                updated_values["extra_information"] = new_extra_info
                if old_extra_info:
                    changes_description.append("Extra Information has been modified")
                else:
                    changes_description.append("Extra Information has been added")

            if not changes_description:
                messagebox.showinfo(
                    "No Changes", "No changes were made to the member details."
                )
                return

            confirm_message = "The following changes will be made:\n\n"
            confirm_message += "\n".join(changes_description)
            confirm_message += "\n\nDo you want to save these changes?"

            if messagebox.askyesno("Confirm Changes", confirm_message):
                member.update(updated_values)
                members_data = []
                for member_id, member in self.family_tree.members.items():
                    member_data = member.copy()
                    member_data["id"] = member.get("id")
                    members_data.append(member_data)

                with open("./data/members.json", "w") as f:
                    json.dump(members_data, f, indent=4)

                self._populate_member_list()
                messagebox.showinfo("Success", "Member details updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update member details: {str(e)}")

    def _remove_member(self):
        if not self.current_member_id:
            messagebox.showinfo("No Selection", "Please select a member to remove.")
            return

        member = self.family_tree.members[self.current_member_id]
        member_name = member.get("name", f"Member {self.current_member_id}")

        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to remove {member_name} from the family tree?\n\nThis will also remove all parent/child relationships associated with this member.",
        ):
            return

        try:
            # Remove the member
            del self.family_tree.members[self.current_member_id]
            members_data = []
            for member_id, member in self.family_tree.members.items():
                member_data = member.copy()
                member_data["id"] = member.get("id")
                members_data.append(member_data)

            with open("./data/members.json", "w") as f:
                json.dump(members_data, f, indent=4)

            self.details_frame.clear_details()
            self.current_member_id = None
            self._populate_member_list()
            messagebox.showinfo(
                "Success", f"{member_name} has been removed from the family tree."
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove member: {str(e)}")

    def _add_member(self):
        AddMemberDialog(self.root, self.family_tree, self._populate_member_list)

    def run(self):
        self.root.mainloop()
