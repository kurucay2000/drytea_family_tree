import tkinter as tk
from tkinter import ttk, messagebox
import json
from utils.validate import validate_parent


class AddMemberDialog:
    def __init__(self, parent, family_tree, callback):
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Family Member")
        self.dialog.geometry("500x700")
        self.dialog.configure(bg="#f0e6ff")  # Light purple background

        # Store references
        self.family_tree = family_tree
        self.callback = callback

        # Configure styles for this dialog
        style = ttk.Style()
        style.configure("Dialog.TFrame", background="#f0e6ff")
        style.configure("Dialog.TLabelframe", background="#f0e6ff")
        style.configure(
            "Dialog.TLabelframe.Label", background="#f0e6ff", foreground="black"
        )
        style.configure(
            "Dialog.TLabel",
            background="#f0e6ff",
            foreground="black",
            font=("Arial", 10),
        )
        style.configure(
            "DialogTitle.TLabel",
            background="#f0e6ff",
            foreground="black",
            font=("Arial", 12, "bold"),
        )
        style.configure("Dialog.TButton", background="#6a0dad", foreground="black")

        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Create main frame
        main_frame = ttk.Frame(self.dialog, padding="10", style="Dialog.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add title
        ttk.Label(
            main_frame, text="Add New Family Member", style="DialogTitle.TLabel"
        ).pack(pady=(0, 10))

        # Create details frame
        details_frame = ttk.LabelFrame(
            main_frame, text="Member Details", style="Dialog.TLabelframe"
        )
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
            ttk.Label(details_frame, text=label_text, style="Dialog.TLabel").grid(
                row=i, column=0, sticky="w", padx=5, pady=2
            )

            if var_key == "gender":
                self.detail_entries[var_key] = ttk.Combobox(
                    details_frame,
                    textvariable=self.detail_vars[var_key],
                    values=["Male", "Female", "Alien", "Other"],
                    state="readonly",
                )
            elif var_key == "id":
                self.detail_entries[var_key] = ttk.Entry(
                    details_frame,
                    textvariable=self.detail_vars[var_key],
                    state="readonly",
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
                )
            else:
                self.detail_entries[var_key] = ttk.Entry(
                    details_frame, textvariable=self.detail_vars[var_key]
                )

            # Configure entry widget colors
            if hasattr(self.detail_entries[var_key], "configure"):
                self.detail_entries[var_key].configure(
                    background="white", foreground="black"
                )

            self.detail_entries[var_key].grid(
                row=i, column=1, sticky="ew", padx=5, pady=2
            )

        # Set next available ID
        current_ids = []
        for member in self.family_tree.members.values():
            member_id = member.get("id", 0)
            try:
                current_ids.append(int(member_id) if member_id else 0)
            except (ValueError, TypeError):
                current_ids.append(0)

        next_id = max(current_ids, default=0) + 1
        self.detail_vars["id"].set(str(next_id))

        # Extra Information Text Area
        ttk.Label(details_frame, text="Extra Information:", style="Dialog.TLabel").grid(
            row=len(regular_fields), column=0, sticky="nw", padx=5, pady=2
        )

        # Create text frame for extra information
        text_frame = ttk.Frame(details_frame, style="Dialog.TFrame")
        text_frame.grid(
            row=len(regular_fields), column=1, sticky="nsew", padx=5, pady=2
        )

        # Configure text widget with purple theme
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

        scrollbar = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.extra_info_text.yview
        )

        self.extra_info_text.configure(yscrollcommand=scrollbar.set)
        self.extra_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure grid weights for details frame
        details_frame.grid_columnconfigure(1, weight=1)

        # Buttons frame
        button_frame = ttk.Frame(main_frame, style="Dialog.TFrame")
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # Cancel and Add Member buttons with purple theme
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            style="Dialog.TButton",
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            button_frame,
            text="Add Member",
            command=self._add_member,
            style="Dialog.TButton",
        ).pack(side=tk.RIGHT, padx=5)

    def _add_member(self):
        """Process the form data and add the member"""
        values = {}

        # Get values from entry fields
        for field_name, var in self.detail_vars.items():
            value = var.get().strip()
            # Convert ID to integer
            if field_name == "id" and value:
                value = int(value)
            if value:  # Only include non-empty values
                if field_name == "age":
                    valid_ages = [
                        "Infant",
                        "Toddler",
                        "Child",
                        "Teen",
                        "Young Adult",
                        "Adult",
                        "Elder",
                    ]
                    if value.title() not in valid_ages:
                        messagebox.showerror(
                            "Error", f"Age must be one of: {', '.join(valid_ages)}"
                        )
                        return

                # Validate parent fields
                if field_name in ["father", "mother"]:
                    if not validate_parent(value, self.family_tree):
                        messagebox.showerror(
                            "Error",
                            f"The specified {field_name} '{value}' does not exist in the family tree",
                        )
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
