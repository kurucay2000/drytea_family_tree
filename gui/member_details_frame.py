import tkinter as tk
from tkinter import ttk, messagebox
from utils.validate import validate_parent
import json


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
        # Create main details frame with purple theme
        details_frame = ttk.LabelFrame(parent, text="Member Details", padding="10")
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Regular fields with their labels and entries
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

        # Create each field with appropriate styling
        for i, (label_text, var_key) in enumerate(regular_fields):
            # Label
            ttk.Label(details_frame, text=label_text, style="TLabel").grid(
                row=i, column=0, sticky="w", padx=5, pady=2
            )

            # Create appropriate widget based on field type
            if var_key == "gender":
                self.detail_entries[var_key] = ttk.Combobox(
                    details_frame,
                    textvariable=self.detail_vars[var_key],
                    values=["Male", "Female", "Alien", "Other"],
                    state="readonly",
                    style="TCombobox",
                )
            elif var_key == "id":
                self.detail_entries[var_key] = ttk.Entry(
                    details_frame,
                    textvariable=self.detail_vars[var_key],
                    state="readonly",
                    style="TEntry",
                )
            elif var_key == "age":
                self.detail_entries[var_key] = ttk.Combobox(
                    details_frame,
                    textvariable=self.detail_vars[var_key],
                    values=[
                        "Infant",
                        "Toddler",
                        "Child",
                        "Teen",
                        "Young Adult",
                        "Adult",
                        "Elder",
                    ],
                    state="readonly",
                    style="TCombobox",
                )
            else:
                self.detail_entries[var_key] = ttk.Entry(
                    details_frame,
                    textvariable=self.detail_vars[var_key],
                    style="TEntry",
                )

            # Grid the entry widget
            self.detail_entries[var_key].grid(
                row=i, column=1, sticky="ew", padx=5, pady=2
            )

        # Extra Information section
        ttk.Label(details_frame, text="Extra Information:", style="TLabel").grid(
            row=len(regular_fields), column=0, sticky="nw", padx=5, pady=2
        )

        # Create frame for text area and scrollbar
        text_frame = ttk.Frame(details_frame)
        text_frame.grid(
            row=len(regular_fields), column=1, sticky="nsew", padx=5, pady=2
        )

        # Text area with purple theme
        self.extra_info_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            height=8,
            width=40,
            bg="white",
            fg="black",
            insertbackground="black",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Arial", 10),
        )

        # Scrollbar for text area
        scrollbar = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.extra_info_text.yview
        )

        # Configure text widget scrollbar
        self.extra_info_text.configure(yscrollcommand=scrollbar.set)

        # Pack text widget and scrollbar
        self.extra_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure grid weights
        details_frame.grid_columnconfigure(1, weight=1)

        # Save Changes button
        self.save_changes_btn = ttk.Button(
            details_frame,
            text="Save Changes",
            command=self.save_changes,
            style="TButton",
        )
        self.save_changes_btn.grid(
            row=len(regular_fields) + 1, column=0, columnspan=2, pady=10
        )

        # Initially hide the save button
        self.save_changes_btn.grid_remove()

    def clear_details(self):
        """Clear all fields in the details frame"""
        # Clear all StringVar fields
        for var in self.detail_vars.values():
            var.set("")

        # Clear the extra information text widget
        self.extra_info_text.delete("1.0", tk.END)

        # Hide the save button since there's no member selected
        self.save_changes_btn.grid_remove()

        # Reset current member ID
        self.current_member_id = None

    def update_details(self, member):
        """Update the details frame with member information"""
        # Store the original member data for accurate change detection
        self.original_member = member.copy()

        for key, var in self.detail_vars.items():
            value = member.get(key)
            var.set(str(value) if value is not None else "")

        # Clear and update extra information text
        self.extra_info_text.delete("1.0", tk.END)
        if member.get("extra_information"):
            self.extra_info_text.insert("1.0", member["extra_information"])

        self.save_changes_btn.grid()
        self.current_member_id = member.get("id")

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
            # Skip ID field since it's read-only
            if field_name == "id":
                continue

            new_value = var.get().strip()
            old_value = current_member.get(field_name, "")

            # Convert to strings only for comparison if both values exist
            old_str = str(old_value) if old_value is not None else ""
            new_str = str(new_value) if new_value else ""

            if new_str != old_str:
                # Age validation
                if field_name == "age" and new_value:
                    valid_ages = [
                        "Infant",
                        "Toddler",
                        "Child",
                        "Teen",
                        "Young Adult",
                        "Adult",
                        "Elder",
                    ]
                    if new_value.title() not in valid_ages:
                        messagebox.showerror(
                            "Error", f"Age must be one of: {', '.join(valid_ages)}"
                        )
                        return

                # Parent validation
                if field_name in ["father", "mother"] and new_value:
                    if not validate_parent(new_value, self.family_tree):
                        messagebox.showerror(
                            "Error",
                            f"The specified {field_name} '{new_value}' does not exist in the family tree",
                        )
                        # Clear the invalid parent field
                        self.detail_vars[field_name].set("")
                        return

                # Handle both setting and clearing of values
                field_label = field_name.replace("_", " ").title()
                if new_value:
                    updated_values[field_name] = new_value
                    if old_value:
                        changes_description.append(
                            f"{field_label}: '{old_value}' → '{new_value}'"
                        )
                    else:
                        changes_description.append(
                            f"{field_label}: Added '{new_value}'"
                        )
                else:
                    # Explicitly set to None when clearing a field
                    updated_values[field_name] = None
                    if old_value:
                        changes_description.append(
                            f"{field_label}: Removed '{old_value}'"
                        )

        # Get extra information changes
        new_extra_info = self.extra_info_text.get("1.0", tk.END).strip()
        old_extra_info = current_member.get("extra_information", "")
        if new_extra_info != old_extra_info:
            if new_extra_info:
                updated_values["extra_information"] = new_extra_info
                if old_extra_info:
                    changes_description.append(
                        f"Extra Information: '{old_extra_info}' → '{new_extra_info}'"
                    )
                else:
                    changes_description.append(
                        f"Extra Information: Added '{new_extra_info}'"
                    )
            else:
                updated_values["extra_information"] = None
                if old_extra_info:
                    changes_description.append(
                        f"Extra Information: Removed '{old_extra_info}'"
                    )

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

            # Call the callback without triggering another save operation
            if self.save_callback:
                self.save_callback(skip_save_check=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update member details: {str(e)}")
