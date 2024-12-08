import tkinter as tk
from tkinter import ttk, messagebox
from utils.validate import validate_parent


class MemberDetailsFrame:
    def __init__(self, parent, family_tree, save_callback):
        self.family_tree = family_tree
        self.save_callback = save_callback
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
        self._create_widgets(parent)

    def _create_widgets(self, parent):
        details_frame = ttk.LabelFrame(parent, text="Member Details")
        details_frame.pack(fill=tk.BOTH, expand=True)

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

        ttk.Label(details_frame, text="Extra Information:").grid(
            row=len(regular_fields), column=0, sticky="nw", padx=5, pady=2
        )
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
        details_frame.grid_columnconfigure(1, weight=1)

        self.save_changes_btn = ttk.Button(
            details_frame, text="Save Changes", command=self.save_callback
        )
        self.save_changes_btn.grid(
            row=len(regular_fields) + 1, column=0, columnspan=2, pady=10
        )
        self.save_changes_btn.grid_remove()

    def update_details(self, member):
        for key, var in self.detail_vars.items():
            if key == "id":
                id_value = member.get("id", "ID Missing")
                var.set(str(id_value))
            else:
                value = member.get(key)
                var.set(str(value) if value is not None else "")
        self.extra_info_text.delete("1.0", tk.END)
        if member.get("extra_information"):
            self.extra_info_text.insert("1.0", member["extra_information"])
        self.save_changes_btn.grid()
        self.current_member_id = member.get("id")

    def clear_details(self):
        for var in self.detail_vars.values():
            var.set("")
        self.extra_info_text.delete("1.0", tk.END)
        self.save_changes_btn.grid_remove()
        self.current_member_id = None

    def save_changes(self):
        if self.current_member_id is None:
            return

        current_member = None
        for member in self.family_tree.members.values():
            if str(member.get("id")) == str(self.current_member_id):
                current_member = member
                break

        if not current_member:
            messagebox.showerror("Error", "Cannot find member to update")
            return

        updated_values = {}
        changes_description = []

        for field_name, var in self.detail_vars.items():
            new_value = var.get().strip()
            # Convert ID to integer
            if field_name == "id" and new_value:
                new_value = int(new_value)
            old_value = (
                str(current_member.get(field_name, ""))
                if current_member.get(field_name) is not None
                else ""
            )

            if new_value != old_value:
                # Age validation
                if field_name == "age" and new_value:
                    try:
                        value = int(float(new_value))
                        if value < 0:
                            messagebox.showerror("Error", "Age cannot be negative")
                            return
                    except ValueError:
                        messagebox.showerror("Error", "Age must be a valid number")
                        return

                # Parent validation
                if field_name in ["father", "mother"] and new_value:
                    if not validate_parent(new_value, self.family_tree):
                        messagebox.showerror(
                            "Error",
                            f"The specified {field_name} '{new_value}' does not exist in the family tree",
                        )
                        return

                if new_value:
                    updated_values[field_name] = new_value
                    field_label = field_name.replace("_", " ").title()
                    if old_value:
                        changes_description.append(
                            f"{field_label}: '{old_value}' → '{new_value}'"
                        )
                    else:
                        changes_description.append(
                            f"{field_label}: Added '{new_value}'"
                        )

        # Get extra information changes
        new_extra_info = self.extra_info_text.get("1.0", tk.END).strip()
        old_extra_info = current_member.get("extra_information", "")
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

        # Confirm changes with user
        confirm_message = "The following changes will be made:\n\n" + "\n".join(
            changes_description
        )
        if not messagebox.askyesno(
            "Confirm Changes",
            confirm_message + "\n\nDo you want to save these changes?",
        ):
            return

        try:
            # Update member
            current_member.update(updated_values)

            # Save to file
            members_data = [member for member in self.family_tree.members.values()]
            with open("./data/members.json", "w") as f:
                json.dump(members_data, f, indent=4)

            messagebox.showinfo("Success", "Member details updated successfully!")
            self.save_callback()  # Refresh the UI

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update member details: {str(e)}")
