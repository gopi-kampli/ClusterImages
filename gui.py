import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from main import ClusterImages

class Application(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.ci = ClusterImages()

        self.title("ImageClusterDL")
        self.minsize(640, 400)

        self.labelFrame = ttk.LabelFrame(self, text="Open Folder")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)

        self.scanFrame = ttk.LabelFrame(self, text="Scan for images")
        self.scanFrame.grid(column=0, row=2, padx=20, pady=20)

        self.create_browse_widget()
        self.create_scan_widget()
        self.create_cluster_widget()

    def create_browse_widget(self):
        self.browse_button = tk.Button(self)
        self.button = ttk.Button(self.labelFrame, text="Browse", command=self.folder_dialog)
        self.button.grid(column=0, row=1)


    def create_scan_widget(self):
        self.scan_button = ttk.Button(self.scanFrame,text="Scan for images", command=self.scan_images)
        self.scan_button.grid(column=0, row=1)


    def create_cluster_widget(self):
        self.cluster_button = ttk.Button(self.scanFrame, text="Seperate images to clusters", command=self.seperate_images)
        self.cluster_button.grid(column=0, row=2,padx=10, pady=10)


    def folder_dialog(self):
        self.filename = filedialog.askdirectory()
        self.label = ttk.Label(self.labelFrame, text="")
        self.label.grid(column=2, row=1)
        self.label.configure(text=self.filename,justify='right')

    def scan_images(self):
        self.images_found = self.ci.images_found_amount(self.filename)
        self.label = ttk.Label(self.scanFrame, text="")
        self.label.grid(column=2, row=1)
        self.label.configure(text=self.images_found)


    def seperate_images(self):
        self.ci.cluster_to_folders(self.filename)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

