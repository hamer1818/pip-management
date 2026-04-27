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
    
    # PyInstaller parametreleri - RESTART LOOP FIX EXTREME
    pyinstaller_args = [
        'main.py',
        '--onefile',                    # Tek dosya halinde
        '--windowed',                   # Console penceresi gösterme  
        '--name=ModernPipManager',      # Exe dosya adı
        '--icon=icon.ico',              # İkon dosyası (varsa)
        '--add-data=pip_manager;pip_manager',  # pip_manager klasörünü dahil et
        '--add-data=version.py;.',      # version.py dosyasını dahil et
        
        # CRITICAL: Restart loop tamamen önleme parametreleri
        '--noupx',                      # UPX sıkıştırma kapatma (sorun yaratabilir)
        '--strip',                      # Debug sembollerini kaldır
        '--exclude-module=unittest',    # Gereksiz modülleri hariç tut
        '--exclude-module=test',
        '--exclude-module=tkinter.test',
        '--exclude-module=lib2to3',
        '--exclude-module=xmlrpc',
        '--exclude-module=pydoc',
        
        # ANTI-RESTART: Multiprocessing modüllerini kontrollü dahil et
        '--hidden-import=multiprocessing',
        '--hidden-import=multiprocessing.spawn',
        '--hidden-import=multiprocessing.util',
        '--hidden-import=multiprocessing.pool',
        '--hidden-import=multiprocessing.queues',
        '--hidden-import=multiprocessing.context',
        
        # SUBPROCESS güvenlik import'ları
        '--hidden-import=subprocess',
        '--hidden-import=threading',
        
        # Ana GUI import'lar
        '--hidden-import=ttkbootstrap', 
        '--hidden-import=ttkbootstrap.themes',
        '--hidden-import=ttkbootstrap.validation',
        '--hidden-import=ttkbootstrap.constants',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk', 
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=json',
        '--hidden-import=urllib',
        '--hidden-import=urllib.request',
        '--hidden-import=urllib.parse',
        '--hidden-import=urllib.error',
        '--hidden-import=datetime',
        '--hidden-import=sys',
        '--hidden-import=os',
        '--hidden-import=pathlib',
        '--hidden-import=tempfile',
        
        # Process control için
        '--hidden-import=psutil',       # Process kontrol (opsiyonel)
        
        # Collect all önemli paketler
        '--collect-all=ttkbootstrap',   # ttkbootstrap'ın tüm dosyalarını dahil et
        '--collect-all=PIL',            # Pillow'un tüm dosyalarını dahil et
        
        # EXTREME build ayarları - restart loop önleme
        '--noconfirm',                  # Onay sorma
        '--clean',                      # Cache'i temizle
        '--debug=imports',              # Import debug için
        '--runtime-tmpdir=.',           # Runtime temp dir
        '--bootloader-ignore-signals',  # Signal handling fix
    ]
    
    # İkon dosyası yoksa parametreyi kaldır
    if not os.path.exists("icon.ico"):
        pyinstaller_args = [arg for arg in pyinstaller_args if not arg.startswith('--icon')]
    
    print("[BUILD] PyInstaller ile exe dosyasi olusturuluyor...")
    print("[BUILD] RESTART LOOP FIX parametreleri eklendi")
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
            print("[INFO] Restart loop fix uygulanmis durumda")
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