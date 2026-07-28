# 🇨🇳 China Mobile Number Extractor

A simple GUI application to extract valid Chinese mobile numbers from text.

## ✨ Features

- 📋 Paste text from clipboard
- 📂 Load text files
- 🔍 Extract 11-digit China mobile numbers (starting with 1, second digit 3-9)
- 💾 Export results to text file
- 🎨 Clean, modern GUI interface

## 🚀 How to Use

1. Paste text or load a file
2. Click "Extract" 
3. All valid China mobile numbers will appear
4. Click "Export" to save results

## 📱 Valid Number Format

- 11 digits
- Starts with 1
- Second digit: 3, 4, 5, 6, 7, 8, or 9
- Examples: 13812345678, 15907525372

## 🛠️ Build from Source

```bash
# Install dependencies
pip install pyinstaller

# Build executable
python -m PyInstaller --onefile --noconsole --windowed extractor.py