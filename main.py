import tkinter as tk
import os
import sys

# Windows'ta DPI farkındalığı için, eğer kütüphane varsa
if os.name == 'nt':
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1) 
    except (ImportError, AttributeError): 
        pass 

from pip_manager.app import ModernPipManager

def main():
    """Ana uygulama fonksiyonu"""
    root = tk.Tk()
    _app_instance = ModernPipManager(root) 
    
    # Pencereyi ekranın ortasında başlat
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x_main_pos = (root.winfo_screenwidth() // 2) - (width // 2) 
    y_main_pos = (root.winfo_screenheight() // 2) - (height // 2) 
    root.geometry(f'{width}x{height}+{x_main_pos}+{y_main_pos}')
    
    # Minimum pencere boyutunu ayarla
    root.minsize(1000, 700) 
    
    # Tkinter ana döngüsünü başlat
    root.mainloop()

if __name__ == "__main__":
    main()
