import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# --- Extraction Logic (Duplicates Removed) ---
def extract_china_numbers(text):
    # Matches +8613xxxxxxxxx or 13xxxxxxxxx (starts with 13-19)
    pattern = r'(?:\+86)?1[3-9]\d{9}\b'
    matches = re.findall(pattern, text)
    
    # Remove duplicates while preserving original order
    return list(dict.fromkeys(matches))

# --- Button Functions ---
def paste_text():
    try:
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, root.clipboard_get())
    except tk.TclError:
        messagebox.showwarning("Clipboard Empty", "Nothing found in clipboard to paste.")

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, f.read())

def process_text():
    content = text_box.get("1.0", tk.END)
    numbers = extract_china_numbers(content)
    
    result_box.delete("1.0", tk.END)
    
    if numbers:
        for num in numbers:
            result_box.insert(tk.END, f"{num}\n")
        results_label.config(text=f"Results ({len(numbers)} Unique Numbers Found)")
    else:
        results_label.config(text="Results (0 Numbers Found)")

def clear_all():
    text_box.delete("1.0", tk.END)
    result_box.delete("1.0", tk.END)
    results_label.config(text="Results (0 Numbers Found)")

def export_file():
    content = result_box.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Export Failed", "No extracted numbers to save!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt"), ("CSV File", "*.csv")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Success", "Numbers exported successfully!")

# --- UI Setup ---
root = tk.Tk()
root.title("China Number Extractor")
root.geometry("650x550")
root.configure(bg="#0c0d1a")

# Styling Colors
BG_DARK = "#0c0d1a"
CARD_BG = "#131527"
TEXT_COLOR = "#ffffff"
BTN_BG = "#1b1e36"
BTN_TEXT = "#ffffff"

# Header Banner
header_frame = tk.Frame(root, bg=CARD_BG, pady=15)
header_frame.pack(fill="x", padx=20, pady=(15, 10))

header_title = tk.Label(
    header_frame, 
    text="China Number Extractor", 
    font=("Segoe UI", 20, "bold"), 
    fg=TEXT_COLOR, 
    bg=CARD_BG
)
header_title.pack()

# Toolbar Buttons
toolbar = tk.Frame(root, bg=BG_DARK)
toolbar.pack(fill="x", padx=20, pady=5)

def create_btn(parent, text, command):
    return tk.Button(
        parent, text=text, command=command,
        bg=BTN_BG, fg=BTN_TEXT, activebackground="#2c3057", activeforeground="#ffffff",
        font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=8, cursor="hand2"
    )

create_btn(toolbar, "📋 Paste", paste_text).pack(side="left", padx=(0, 5))
create_btn(toolbar, "📂 Load File", load_file).pack(side="left", padx=5)
create_btn(toolbar, "🔍 Extract", process_text).pack(side="left", padx=5)
create_btn(toolbar, "🗑 Clear", clear_all).pack(side="left", padx=5)
create_btn(toolbar, "💾 Export", export_file).pack(side="left", padx=5)

# Enter Text Section
tk.Label(root, text="Enter Text", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg=BG_DARK).pack(anchor="w", padx=20, pady=(10, 2))
text_box = tk.Text(root, height=7, bg=CARD_BG, fg="#a0a5c0", insertbackground="white", bd=0, padx=10, pady=10, font=("Consolas", 10))
text_box.pack(fill="x", padx=20)
text_box.insert("1.0", "Paste your text here...")

# Results Section
results_label = tk.Label(root, text="Results (0 Numbers Found)", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg=BG_DARK)
results_label.pack(anchor="w", padx=20, pady=(15, 2))

result_box = tk.Text(root, height=9, bg=CARD_BG, fg="#ffffff", insertbackground="white", bd=0, padx=10, pady=10, font=("Consolas", 10))
result_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))

root.mainloop()