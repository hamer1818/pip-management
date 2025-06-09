import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import sys
import multiprocessing
from version import __version__, __app_name__

# Windows'ta DPI farkındalığı için, eğer kütüphane varsa
if os.name == 'nt':
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1) 
    except (ImportError, AttributeError): 
        pass 

def main():
    """Ana uygulama fonksiyonu"""
    try:
        # PyInstaller ile oluşturulan exe'de multiprocessing sorunlarını önle
        if getattr(sys, 'frozen', False):
            # Exe dosyası olarak çalışıyoruz
            multiprocessing.freeze_support()
        
        # Import'u main fonksiyonu içinde yaparak circular import sorunlarını önle
        from pip_manager.app import ModernPipManager
        
        # ttkbootstrap stil teması ile uygulama oluştur
        app = ttk.Window(
            title=f"🐍 {__app_name__} v{__version__}",
            themename="darkly",  # Modern dark tema
            size=(1200, 800),
            resizable=(True, True)
        )
        
        # Pencereyi ekranın ortasında başlat
        app.place_window_center()
        
        # Minimum pencere boyutunu ayarla
        app.minsize(1000, 700) 
        
        # Uygulama instance'ını oluştur
        try:
            _app_instance = ModernPipManager(app) 
        except Exception as e:
            print(f"[ERROR] Uygulama başlatılırken hata: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Ana döngüyü başlat
        app.mainloop()
        
    except Exception as e:
        print(f"[ERROR] Ana uygulama hatası: {e}")
        import traceback
        traceback.print_exc()
        # Hata durumunda kullanıcıya bilgi ver
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()  # Ana pencereyi gizle
            messagebox.showerror(
                "Uygulama Hatası", 
                f"Uygulama başlatılırken bir hata oluştu:\n\n{str(e)}\n\nDetaylar için konsolu kontrol edin."
            )
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    # PyInstaller multiprocessing desteği
    multiprocessing.freeze_support()
    main()
