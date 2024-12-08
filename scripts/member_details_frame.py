import tkinter as tk
from tkinter import ttk


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

    def clear_details(self):
        for var in self.detail_vars.values():
            var.set("")
        self.extra_info_text.delete("1.0", tk.END)
        self.save_changes_btn.grid_remove()
