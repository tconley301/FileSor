<p align="center">
  <img src="assets/filesor_ui.png" width="400">
</p>

# FileSor

FileSor is a desktop application that organizes files into user-defined folders
based on allowed file extensions. Built with **Python** and **PySide6**, the app
provides a clean UI and drag-and-drop support for easy file sorting.

---

## Features
- Custom folder rules by file extension  
- Drag-and-drop sorting box  
- Clean, modern UI built with Qt Designer  
- Rule management (add / edit / remove folders)  

---

## Setup

### 1. Clone repo

    git clone https://github.com/tconley301/FileSor.git
    cd FileSor

### 2. Create and Activate Virtual Environment

    python -m venv .venv
    .venv\Scripts\activate (Windows)
    source .venv/bin/activate (macOS / Linux)

### 3. Install Dependencies 
    
    pip install -r req.txt

### 4. Restart the terminal
Close and reopen the terminal.  
You should now see something like:

    (.venv) PS C:\Users\...
    
---

## Running the App

    python src/core/app_init.py
