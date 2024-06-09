import os
import tkinter as tk
from tkinter import filedialog, ttk

class FolderSizeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Folder Size Viewer")
        self.geometry("800x500")

        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("1", "2", "3")
        self.tree.column("#0", width=200)
        self.tree.column("1", width=200)
        self.tree.column("2", width=100)
        self.tree.column("3", width=100)
        self.tree.heading("#0", text="Name")
        self.tree.heading("1", text="Path")
        self.tree.heading("2", text="Size (MB)")
        self.tree.heading("3", text="Size (GB)")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self.show_folder_details)

        self.btn_select_folder = tk.Button(self, text="Select Folder", command=self.select_folder)
        self.btn_select_folder.pack(pady=10)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.add_folder_to_tree(folder_path)

    def add_folder_to_tree(self, folder_path):
        folder_size = get_folder_size(folder_path)
        folder_name = os.path.basename(folder_path)
        self.tree.insert("", "end", text=folder_name, values=(folder_path, f"{folder_size/1024**2:.3f}", f"{folder_size / (1024 ** 3):.3f}"))

    def show_folder_details(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            folder_path = self.tree.item(selected_item)["values"][0]
            self.display_folder_contents(folder_path)

    def display_folder_contents(self, folder_path):
        for item in self.tree.get_children(""):
            self.tree.delete(item)

        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                file_size = os.path.getsize(file_path)
                self.tree.insert("", "end", text=filename, values=(file_path, f"{file_size/1024**2:.3f}", f"{file_size / (1024 ** 3):.3f}"))

def get_folder_size(folder_path):
    """
    獲取指定資料夾的總大小(單位為 bytes)
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(file_path)
            except FileNotFoundError:
                print(f"Error getting size of {file_path}")
    return total_size

if __name__ == "__main__":
    app = FolderSizeApp()
    app.mainloop()