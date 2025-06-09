import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import sys
from version import __version__, __app_name__

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
    # ttkbootstrap stil teması ile uygulama oluştur
    app = ttk.Window(
        title=f"🐍 {__app_name__} v{__version__}",
        themename="darkly",  # Modern dark tema
        size=(1200, 800),
        resizable=(True, True)
    )
    
    _app_instance = ModernPipManager(app) 
    
    # Pencereyi ekranın ortasında başlat
    app.place_window_center()
    
    # Minimum pencere boyutunu ayarla
    app.minsize(1000, 700) 
    
    # Ana döngüyü başlat
    app.mainloop()

if __name__ == "__main__":
    main()
