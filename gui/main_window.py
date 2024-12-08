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
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.current_member_id = None
        self.member_ids = []
        self._create_widgets()

    def _create_widgets(self):
        left_frame = ttk.Frame(self.main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Label(left_frame, text="Family Members", font=("Arial", 12, "bold")).pack()
        self.member_listbox = tk.Listbox(left_frame, width=30)
        self.member_listbox.pack(fill=tk.BOTH, expand=True)
        self.member_listbox.bind("<<ListboxSelect>>", self._on_member_select)
        self._populate_member_list()

        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.details_frame = MemberDetailsFrame(
            right_frame, self.family_tree, self._save_member_changes
        )

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
        current_selection = self.member_listbox.curselection()
        self.member_listbox.delete(0, tk.END)
        self.member_ids = []
        sorted_members = sorted(
            self.family_tree.members.items(),
            key=lambda x: int(x[1].get("id", float("inf")))
            if isinstance(x[1].get("id"), str)
            else x[1].get("id", float("inf")),
        )
        for member_id, member in sorted_members:
            name = member.get("name", "Unknown")
            self.member_listbox.insert(tk.END, name)
            self.member_ids.append(member_id)
        if current_selection:
            self.member_listbox.selection_set(current_selection)

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

    def _save_member_changes(self):
        if self.current_member_id is None:
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
