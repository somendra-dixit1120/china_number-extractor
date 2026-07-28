import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import re
from datetime import datetime

class PhoneExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🇨🇳 China Phone Number Extractor")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        self.colors = {
            'bg': '#f0f4f8',
            'primary': '#1a73e8',
            'secondary': '#34a853',
            'accent': '#ea4335',
            'dark': '#202124',
            'light': '#ffffff',
            'border': '#dadce0'
        }
        
        self.root.configure(bg=self.colors['bg'])
        self.extracted_numbers = []
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=70)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🇨🇳 CHINA MOBILE NUMBER EXTRACTOR",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(pady=18)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        buttons = [
            ("📋 Paste", self.paste_text, self.colors['primary']),
            ("📂 Load File", self.load_file, self.colors['secondary']),
            ("🗑️ Clear", self.clear_all, self.colors['accent']),
            ("🔍 Extract", self.extract_numbers, '#fbbc04'),
            ("💾 Export", self.export_results, '#9c27b0')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=('Segoe UI', 10),
                bg=color,
                fg='white' if color != '#fbbc04' else 'black',
                padx=15,
                pady=6,
                command=command,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        # Input Area
        input_frame = tk.LabelFrame(
            main_frame,
            text="📝 Enter Text",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['dark']
        )
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=6,
            font=('Consolas', 10),
            wrap=tk.WORD,
            bg='white'
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.input_text.insert('1.0', "Paste your text here...")
        self.input_text.bind('<FocusIn>', self.on_focus_in)
        self.input_text.bind('<FocusOut>', self.on_focus_out)
        
        # Results Area
        results_frame = tk.LabelFrame(
            main_frame,
            text="📊 Results",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['dark']
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=10,
            font=('Consolas', 10),
            wrap=tk.WORD,
            bg='#fafafa'
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status Bar
        status_frame = tk.Frame(self.root, bg=self.colors['border'], height=28)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            status_frame,
            text="✅ Ready",
            font=('Segoe UI', 9),
            bg=self.colors['border'],
            fg=self.colors['dark']
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=3)
        
        self.count_label = tk.Label(
            status_frame,
            text="Found: 0",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['border'],
            fg=self.colors['primary']
        )
        self.count_label.pack(side=tk.RIGHT, padx=10, pady=3)
    
    def on_focus_in(self, event):
        if self.input_text.get('1.0', 'end-1c') == "Paste your text here...":
            self.input_text.delete('1.0', tk.END)
    
    def on_focus_out(self, event):
        if not self.input_text.get('1.0', 'end-1c').strip():
            self.input_text.insert('1.0', "Paste your text here...")
    
    def paste_text(self):
        try:
            text = self.root.clipboard_get()
            self.input_text.delete('1.0', tk.END)
            self.input_text.insert('1.0', text)
            self.status_label.config(text="✅ Text pasted!")
        except:
            messagebox.showerror("Error", "No text in clipboard!")
    
    def load_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.delete('1.0', tk.END)
                self.input_text.insert('1.0', content)
                self.status_label.config(text=f"✅ Loaded: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
    
    def clear_all(self):
        self.input_text.delete('1.0', tk.END)
        self.results_text.delete('1.0', tk.END)
        self.extracted_numbers = []
        self.count_label.config(text="Found: 0")
        self.status_label.config(text="🗑️ Cleared")
    
    def extract_china_numbers(self, text):
        """Extract ONLY valid China mobile numbers (11 digits, starting with 1)"""
        # Pattern for China mobile: 11 digits, starts with 1, second digit 3-9
        # Handles: +86, 0086, or nothing before the number
        patterns = [
            r'(?:\+86|0086)?\s*1[3-9]\d{9}\b',  # Standard: +86 13812345678
            r'(?:\+86|0086)?\s*1[3-9]\d{2}[\s-]?\d{4}[\s-]?\d{4}\b',  # With spaces/dashes
        ]
        
        numbers = []
        seen = set()
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Clean the number (remove spaces, dashes, +86, 0086)
                clean = re.sub(r'[\s-]', '', match)
                # Remove +86 or 0086 if present
                clean = re.sub(r'^\+86|^0086', '', clean)
                
                # Only keep valid 11-digit China mobile numbers
                if len(clean) == 11 and clean[0] == '1' and clean[1] in '3456789':
                    if clean not in seen:
                        seen.add(clean)
                        # Keep original format for display
                        numbers.append(match)
        
        return numbers
    
    def extract_numbers(self):
        text = self.input_text.get('1.0', 'end-1c').strip()
        
        if text == "Paste your text here..." or not text:
            messagebox.showwarning("Warning", "Please enter text first!")
            return
        
        self.status_label.config(text="⏳ Extracting...")
        self.root.update()
        
        # Extract numbers
        self.extracted_numbers = self.extract_china_numbers(text)
        
        # Display results - JUST NUMBERS, NO COUNTING
        self.results_text.delete('1.0', tk.END)
        
        if not self.extracted_numbers:
            self.results_text.insert('1.0', "No China mobile numbers found.\n\n")
            self.results_text.insert('1.0', "Valid format: 11 digits starting with 1\n")
            self.results_text.insert('1.0', "Example: 13812345678")
            self.count_label.config(text="Found: 0")
            self.status_label.config(text="❌ No numbers found")
            return
        
        # Show ONLY the numbers, one per line, NO numbering
        for number in self.extracted_numbers:
            self.results_text.insert('1.0', number + "\n")
        
        # Show count in status bar only
        self.count_label.config(text=f"Found: {len(self.extracted_numbers)}")
        self.status_label.config(text=f"✅ Extracted {len(self.extracted_numbers)} numbers")
        
        # Auto-scroll to top
        self.results_text.see('1.0')
    
    def export_results(self):
        if not self.extracted_numbers:
            messagebox.showwarning("Warning", "No numbers to export!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"china_mobiles_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for number in self.extracted_numbers:
                    f.write(number + "\n")
            
            messagebox.showinfo("Success", f"✅ Saved to:\n{filename}")
            self.status_label.config(text=f"💾 Exported: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

def main():
    root = tk.Tk()
    app = PhoneExtractorApp(root)
    
    # Center window
    root.update_idletasks()
    width = 700
    height = 500
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()