import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from datetime import datetime
from PIL import Image, ImageTk, UnidentifiedImageError  # Add UnidentifiedImageError

class DateRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Date Renamer")
        self.folder_path = tk.StringVar()
        self.files = []
        self.current_file_index = 0

        # Date dropdown
        now = datetime.now()
        self.month_var = tk.StringVar(value=str(now.month))
        self.day_var = tk.StringVar(value=str(now.day))
        self.year_var = tk.StringVar(value=str(now.year % 100))

        self.create_widgets()

    def create_widgets(self):
        # Folder selection
        folder_frame = tk.Frame(self.root)
        folder_frame.pack(pady=10)
        tk.Label(folder_frame, text="Folder:").pack(side=tk.LEFT)
        tk.Entry(folder_frame, textvariable=self.folder_path, width=40, state='readonly').pack(side=tk.LEFT, padx=5)
        tk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)

        # Date selection
        date_frame = tk.Frame(self.root)
        date_frame.pack(pady=10)
        tk.Label(date_frame, text="Date:").pack(side=tk.LEFT)
        months = [str(i) for i in range(1, 13)]
        days = [str(i) for i in range(1, 32)]
        years = [str(i).zfill(2) for i in range(0, 100)]
        tk.OptionMenu(date_frame, self.month_var, *months).pack(side=tk.LEFT)
        tk.Label(date_frame, text="-").pack(side=tk.LEFT)
        tk.OptionMenu(date_frame, self.day_var, *days).pack(side=tk.LEFT)
        tk.Label(date_frame, text="-").pack(side=tk.LEFT)
        tk.OptionMenu(date_frame, self.year_var, *years).pack(side=tk.LEFT)

        # Start button
        tk.Button(self.root, text="Start Renaming", command=self.start_renaming).pack(pady=10)

        self.file_frame = tk.Frame(self.root)
        self.file_label = tk.Label(self.file_frame, text="")
        self.file_label.pack(pady=5)
        self.extra_text_var = tk.StringVar()
        self.extra_entry = tk.Entry(self.file_frame, textvariable=self.extra_text_var, width=30)
        self.extra_entry.pack(pady=5)
        self.rename_button = tk.Button(self.file_frame, text="Rename File", command=self.rename_current_file)
        self.rename_button.pack(pady=5)
        # Add Preview Image button
        self.preview_button = tk.Button(self.file_frame, text="Preview Image", command=self.preview_image)
        self.preview_button.pack(pady=5)
        self.file_frame.pack(pady=10)
        self.file_frame.pack_forget()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def start_renaming(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder.")
            return
        self.files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        if not self.files:
            messagebox.showinfo("Info", "No files found in the selected folder.")
            return
        self.current_file_index = 0
        self.file_frame.pack(pady=10)
        self.show_current_file()

    def show_current_file(self):
        if self.current_file_index >= len(self.files):
            messagebox.showinfo("Done", "All files have been renamed.")
            self.file_frame.pack_forget()
            return
        current_file = self.files[self.current_file_index]
        date_str = f"{int(self.month_var.get())}-{int(self.day_var.get())}-{self.year_var.get()}_"
        self.file_label.config(text=f"File: {current_file}\nNew name: {date_str}[your text][original extension]")
        self.extra_text_var.set("")
        self.extra_entry.focus_set()

    def rename_current_file(self):
        folder = self.folder_path.get()
        current_file = self.files[self.current_file_index]
        extra_text = self.extra_text_var.get().strip()
        date_str = f"{int(self.month_var.get())}-{int(self.day_var.get())}-{self.year_var.get()}_"
        name, ext = os.path.splitext(current_file)
        new_name = f"{date_str}{extra_text}{ext}"
        src = os.path.join(folder, current_file)
        dst = os.path.join(folder, new_name)
        try:
            if os.path.exists(dst):
                raise FileExistsError(f"File {new_name} already exists.")
            os.rename(src, dst)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename {current_file}: {e}")
            return
        self.current_file_index += 1
        self.show_current_file()

    def preview_image(self):
        folder = self.folder_path.get()
        if not self.files or self.current_file_index >= len(self.files):
            return
        current_file = self.files[self.current_file_index]
        file_path = os.path.join(folder, current_file)
        supported_exts = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
        if not current_file.lower().endswith(supported_exts):
            messagebox.showerror("Not an image", f"File extension not supported for preview: {current_file}")
            return
        try:
            with open(file_path, 'rb') as f:
                img = Image.open(f)
                img.load()
            max_size = (600, 600)
            img.thumbnail(max_size, Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img)
        except UnidentifiedImageError:
            messagebox.showerror("Not an image", f"Cannot preview this file as an image. The file may be corrupted or not a real image.")
            return
        except Exception as e:
            messagebox.showerror("Not an image", f"Cannot preview this file as an image.\n{e}")
            return
        # Create floating window
        preview_win = tk.Toplevel(self.root)
        preview_win.title(f"Preview: {current_file}")
        label = tk.Label(preview_win, image=img_tk)
        label.image = img_tk
        label.pack()
        preview_win.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = DateRenamerApp(root)
    root.mainloop()
