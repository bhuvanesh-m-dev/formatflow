import shutil
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# 📁 Category → Extensions
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".mkv", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code": [".py", ".c", ".cpp", ".java", ".js", ".html", ".css"],
    "Executables": [".exe", ".msi", ".sh", ".deb", ".apk"]
}

def get_category(ext):
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Others"

def organize_folder(folder_path):
    base = Path(folder_path)
    output = base / "Organized"
    output.mkdir(exist_ok=True)

    moved = 0

    for file in base.rglob("*"):
        if file.is_file() and "Organized" not in file.parts:
            ext = file.suffix.lower()
            category = get_category(ext)

            # Subfolder by extension (PDF, DOCX, etc.)
            ext_folder = ext[1:].upper() if ext else "NO_EXT"

            # Date folder
            date_folder = datetime.fromtimestamp(
                file.stat().st_mtime
            ).strftime("%Y-%m-%d")

            target_dir = output / category / ext_folder / date_folder
            target_dir.mkdir(parents=True, exist_ok=True)

            target_file = target_dir / file.name
            if not target_file.exists():
                shutil.move(str(file), str(target_file))
                moved += 1

    messagebox.showinfo(
        "FormatFlow",
        f"✅ Organization complete!\n\nFiles moved: {moved}\n\nOutput:\n{output}"
    )

def choose_folder():
    folder = filedialog.askdirectory(title="Select Folder to Organize")
    if folder:
        organize_folder(folder)

# 🪟 GUI Window
root = tk.Tk()
root.title("FormatFlow")
root.geometry("380x200")
root.resizable(False, False)

label = tk.Label(
    root,
    text="FormatFlow\nOrganize files by category → type → date",
    font=("Segoe UI", 11),
    pady=20
)
label.pack()

btn = tk.Button(
    root,
    text="📁 Choose Folder",
    width=22,
    font=("Segoe UI", 10),
    command=choose_folder
)
btn.pack(pady=10)

root.mainloop()
