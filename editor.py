import os
import sys
import tkinter as tk
from tkinter import filedialog
import textwrap

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor")
        self.root.iconbitmap("icon.ico")

        self.text = tk.Text(self.root)
        self.text.pack(fill="both", expand=True)

        self.file_name = None
        self.dark_mode = False
        
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Load", command=self.load)
        self.file_menu.add_command(label="Rename", command=self.rename)
        self.file_menu.add_command(label="Delete", command=self.delete)
        
        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        
        self.run_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run Script", command=self.run)

        self.set_dark_mode(self.dark_mode)

    def save(self):
        if self.file_name is None:
            self.file_name = filedialog.asksaveasfilename(defaultextension=".txt")
        with open(self.file_name, "w") as file:
            file.write(self.text.get("1.0", "end"))

    def load(self):
        self.file_name = filedialog.askopenfilename()
        with open(self.file_name, "r") as file:
            self.text.delete("1.0", "end")
            self.text.insert("1.0", file.read())

    def rename(self):
        new_file_name = filedialog.asksaveasfilename(defaultextension=".txt")
        os.rename(self.file_name, new_file_name)
        self.file_name = new_file_name

    def delete(self):
        os.remove(self.file_name)

    def on_configure(self, event):
        self.text.config(scrollregion=self.text.bbox("1.0"))
        self.text.bind("<Configure>", self.on_configure)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.set_dark_mode(self.dark_mode)

    def set_dark_mode(self, dark_mode):
        bg = "black" if dark_mode else "white"
        self.text.config(insertbackground="white") if dark_mode else self.text.config(insertbackground="black")
        fg = "white" if dark_mode else "black"
        self.text.config(bg=bg, fg=fg)

    def run(self):
        code = self.text.get("1.0", "end")
        exec(code)

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()