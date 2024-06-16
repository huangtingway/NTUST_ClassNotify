# notify_system.py
import threading
import tkinter as tk
from tkinter import messagebox
import webCrawler

isClickStartSearch = False

class NotifySystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Class Notify System")
        self.root.geometry("600x400")

        self.class_code_var = tk.StringVar()
        self.driver_path_var = tk.StringVar()
        self.search_list = []
        self.available_list = []

        self.create_widgets()
        self.load()

    def create_widgets(self):
        padx = 10
        pady = 5  # Reduced vertical margin

        self.root.config(padx=padx, pady=pady)

        frame_top = tk.Frame(self.root)
        frame_top.grid(row=0, column=0, columnspan=4, padx=padx, pady=pady, sticky='w')

        tk.Label(frame_top, text="input class code:", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, padx), pady=pady)
        self.entry = tk.Entry(frame_top, textvariable=self.class_code_var, font=('Arial', 12), fg='black', relief='solid', bd=1)
        self.entry.pack(side=tk.LEFT, padx=(0, padx), pady=pady)

        self.add_button = tk.Button(frame_top, text="add", command=self.add_class, font=('Arial', 12), relief='raised', bd=1)
        self.add_button.pack(side=tk.LEFT, padx=(0, padx), pady=pady)

        tk.Button(frame_top, text="delete", command=self.delete_class, font=('Arial', 12), relief='raised', bd=1).pack(side=tk.LEFT, padx=(0, padx), pady=pady)

        # New frame for inputting Chrome driver path
        frame_driver_path = tk.Frame(self.root)
        frame_driver_path.grid(row=1, column=0, columnspan=4, padx=padx, pady=pady, sticky='w')

        tk.Label(frame_driver_path, text="input chrome driver path:", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, padx), pady=pady)
        self.driver_path_entry = tk.Entry(frame_driver_path, textvariable=self.driver_path_var, font=('Arial', 12), fg='black', relief='solid', bd=1, width=40)
        self.driver_path_entry.pack(side=tk.LEFT, padx=(0, padx), pady=pady)

        tk.Label(self.root, text="search class:", font=('Arial', 12)).grid(row=2, column=0, padx=padx, pady=pady, sticky='w')
        self.search_listbox = tk.Listbox(self.root, font=('Arial', 12), height=10, relief='solid', bd=1)
        self.search_listbox.grid(row=3, column=0, padx=padx, pady=pady, sticky='w')
        for item in self.search_list:
            self.search_listbox.insert(tk.END, item)
        self.search_listbox.bind("<<ListboxSelect>>", self.on_search_listbox_select)

        tk.Label(self.root, text="available class:", font=('Arial', 12)).grid(row=2, column=2, padx=padx, pady=pady, sticky='w')
        self.available_listbox = tk.Listbox(self.root, font=('Arial', 12), height=10, relief='solid', bd=1)
        self.available_listbox.grid(row=3, column=2, padx=padx // 2, pady=pady, sticky='w')
        for item in self.available_list:
            self.available_listbox.insert(tk.END, item)
        self.available_listbox.bind("<<ListboxSelect>>", self.on_available_listbox_select)

        frame = tk.Frame(self.root)
        frame.grid(row=4, column=0, columnspan=4, pady=pady, sticky='w')
        self.start_search_btn = tk.Button(frame, text="start search", command=self.start_search, font=('Arial', 12), relief='raised', bd=2)
        self.start_search_btn.grid(row=0, column=2, padx=(0, padx))

    def add_class(self):
        class_code = self.class_code_var.get()
        if class_code and class_code not in self.search_list:
            self.search_list.append(class_code)
            self.search_listbox.insert(tk.END, class_code)
            self.save()
            webCrawler.setClassCode(self.search_list)
            self.class_code_var.set("")
        else:
            messagebox.showwarning("Warning", "Class code already exists or empty.")

    def delete_class(self):
        selected_class = self.search_listbox.curselection()
        if selected_class:
            class_code = self.search_listbox.get(selected_class)
            self.search_listbox.delete(selected_class)
            self.search_list.remove(class_code)
            self.save()
            webCrawler.setClassCode(self.search_list)
            self.class_code_var.set("")
        else:
            messagebox.showwarning("Warning", "No class selected to delete.")

    def save(self):
        with open("available_classes.txt", "w") as f:
            for item in self.search_list:
                f.write(item + "\n")

        with open("driver_path.txt", "w") as f:
            f.write(self.driver_path_var.get())

    def load(self):
        try:
            with open("available_classes.txt", "r") as f:
                self.search_list = [line.strip() for line in f]
            self.search_listbox.delete(0, tk.END)
            for item in self.search_list:
                self.search_listbox.insert(tk.END, item)
            self.update_search_listbox()
        except FileNotFoundError:
            pass

        try:
            with open("driver_path.txt", "r") as f:
                self.driver_path_var.set(f.read().strip())
        except FileNotFoundError:
            pass

    def update_search_listbox(self):
        self.search_listbox.delete(0, tk.END)
        for item in self.search_list:
            self.search_listbox.insert(tk.END, item)

    def start_search(self):
        global isClickStartSearch
        if isClickStartSearch:
            return
        else:
            isClickStartSearch = True

        driver_path = self.driver_path_var.get()
        if not driver_path:
            messagebox.showerror("Error", "Chrome driver path is empty. Please provide a valid path.")
            isClickStartSearch = False
            return

        try:
            webCrawler.setPath(driver_path)
            webCrawler.setClassCode(self.search_list)

            # Create a new thread to start the search
            thread = threading.Thread(target=webCrawler.start_search, args=(self.setAvailableList,))
            thread.start()

            # Save the driver path if the path is correct
            with open("driver_path.txt", "w") as f:
                f.write(driver_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            isClickStartSearch = False

    def on_search_listbox_select(self, event):
        selected_class = self.search_listbox.curselection()
        if selected_class:
            class_code = self.search_listbox.get(selected_class)
            self.class_code_var.set(class_code)

    def on_available_listbox_select(self, event):
        selected_class = self.available_listbox.curselection()
        if selected_class:
            class_code = self.available_listbox.get(selected_class)
            # Handle the selection if needed

    def update_available_listbox(self):
        self.available_listbox.delete(0, tk.END)
        for item in self.available_list:
            self.available_listbox.insert(tk.END, item)

    def setAvailableList(self, availableClass):
        self.available_list = availableClass
        self.update_available_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = NotifySystem(root)
    root.mainloop()
