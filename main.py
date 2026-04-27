#!/usr/bin/env python3
"""
Modern Python Pip Paket Yöneticisi
Gelişmiş pip yönetimi için modern GUI uygulaması
"""

import os
import sys

# CRITICAL: Restart loop fix - HEMEN BAŞTA, HER KOŞULDA
import multiprocessing
if hasattr(sys, 'frozen') and sys.frozen:
    # Exe dosyası olarak çalışıyoruz - CRITICAL restart loop fix
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn', force=True)

# Ana koruma - sadece ana thread çalışsın
if __name__ != "__main__":
    sys.exit(0)

# Process kontrolü - restart loop önleme
def is_already_running():
    """Uygulama zaten çalışıyor mu kontrol et"""
    try:
        import psutil
        current_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['pid'] != current_pid and proc.info['name'] and 'ModernPipManager' in proc.info['name']:
                    return True
                if proc.info['cmdline'] and any('ModernPipManager' in str(cmd) for cmd in proc.info['cmdline']):
                    if proc.info['pid'] != current_pid:
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except ImportError:
        # psutil yoksa basit dosya kilidi kullan
        import tempfile
        lock_file = os.path.join(tempfile.gettempdir(), 'modern_pip_manager.lock')
        try:
            if os.name == 'nt':
                # Windows için
                if os.path.exists(lock_file):
                    try:
                        os.remove(lock_file)
                    except PermissionError:
                        return True
                open(lock_file, 'w').close()
            else:
                # Unix/Linux için
                import fcntl
                f = open(lock_file, 'w')
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (IOError, OSError):
            return True
    return False

# Windows'ta DPI farkındalığı için, eğer kütüphane varsa
if os.name == 'nt':
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1) 
    except (ImportError, AttributeError): 
        pass 

def main():
    """Ana uygulama fonksiyonu - Restart loop korumalı"""
    try:
        # CRITICAL: Sadece exe olarak çalıştığında kontrol et
        if hasattr(sys, 'frozen') and sys.frozen:
            # Zaten çalışıyor mu kontrol et
            if is_already_running():
                print("[INFO] Uygulama zaten calisiyor. Cikiliyor...")
                return
            
            # Multiprocessing restart loop fix
            multiprocessing.freeze_support()
        
        # Import'ları main fonksiyonu içinde yaparak circular import sorunlarını önle
        import ttkbootstrap as ttk
        from version import __version__, __app_name__
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
        
        # Exit handler - restart loop önleme
        def on_closing():
            """Uygulama kapatılırken restart loop önleme"""
            try:
                import tempfile
                lock_file = os.path.join(tempfile.gettempdir(), 'modern_pip_manager.lock')
                if os.path.exists(lock_file):
                    try:
                        os.remove(lock_file)
                    except:
                        pass
            except:
                pass
            app.destroy()
            sys.exit(0)
        
        app.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Uygulama instance'ını oluştur
        try:
            _app_instance = ModernPipManager(app) 
        except Exception as e:
            print(f"[ERROR] Uygulama başlatılırken hata: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Ana döngüyü başlat
        try:
            app.mainloop()
        except KeyboardInterrupt:
            print("[INFO] Kullanici tarafindan sonlandirildi")
        finally:
            on_closing()
        
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
        finally:
            sys.exit(1)

if __name__ == "__main__":
    # FINAL restart loop protection
    try:
        # PyInstaller multiprocessing desteği - TEKRAR CALL
        multiprocessing.freeze_support()
        main()
    except Exception as e:
        print(f"[CRITICAL ERROR] Ana hata: {e}")
        sys.exit(1)
    finally:
        # Kesin çıkış
        os._exit(0)
