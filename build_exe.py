#!/usr/bin/env python3
"""
Modern Python Pip Paket Yöneticisi - Build Script
PyInstaller kullanarak exe dosyası oluşturur
"""

import PyInstaller.__main__
import os
import sys
import shutil
from pathlib import Path

def build_exe():
    """Exe dosyası oluştur"""
    
    # Build klasörünü temizle
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # PyInstaller parametreleri
    pyinstaller_args = [
        'main.py',
        '--onefile',                    # Tek dosya halinde
        '--windowed',                   # Console penceresi gösterme
        '--name=ModernPipManager',      # Exe dosya adı
        '--icon=icon.ico',              # İkon dosyası (varsa)
        '--add-data=pip_manager;pip_manager',  # pip_manager klasörünü dahil et
        '--hidden-import=ttkbootstrap', # Gizli import'ları dahil et
        '--hidden-import=tkinter',
        '--hidden-import=subprocess',
        '--hidden-import=threading',
        '--hidden-import=json',
        '--hidden-import=urllib',
        '--hidden-import=datetime',
        '--collect-all=ttkbootstrap',   # ttkbootstrap'ın tüm dosyalarını dahil et
        '--noconfirm',                  # Onay sorma
        '--clean',                      # Cache'i temizle
    ]
    
    # İkon dosyası yoksa parametreyi kaldır
    if not os.path.exists("icon.ico"):
        pyinstaller_args = [arg for arg in pyinstaller_args if not arg.startswith('--icon')]
    
    print("[BUILD] PyInstaller ile exe dosyasi olusturuluyor...")
    print(f"[BUILD] Parametreler: {' '.join(pyinstaller_args)}")
    
    try:
        # PyInstaller'ı çalıştır
        PyInstaller.__main__.run(pyinstaller_args)
        
        # Başarı kontrolü
        exe_path = Path("dist/ModernPipManager.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"[SUCCESS] Exe dosyasi basariyla olusturuldu!")
            print(f"[INFO] Konum: {exe_path.absolute()}")
            print(f"[INFO] Boyut: {size_mb:.1f} MB")
            return True
        else:
            print("[ERROR] Exe dosyasi olusturulamadi!")
            return False
            
    except Exception as e:
        print(f"[ERROR] Build hatasi: {e}")
        return False

if __name__ == "__main__":
    # Gerekli paketlerin yüklü olup olmadığını kontrol et
    try:
        import PyInstaller
        print(f"[INFO] PyInstaller surumu: {PyInstaller.__version__}")
    except ImportError:
        print("[ERROR] PyInstaller yuklu degil!")
        print("[INFO] Yuklemek icin: pip install pyinstaller")
        sys.exit(1)
    
    # Build işlemini başlat
    success = build_exe()
    sys.exit(0 if success else 1) 