import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sys

from . import ui
from . import handlers
from . import utils

class ModernPipManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Pip Paket Yöneticisi")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Modern tema ayarları
        self.accent_color = '#0078d4' # Örnek değişkeni olarak tanımlandı
        self.setup_theme()
        
        # Ana değişkenler
        self.installed_packages = {}
        
        # create_widgets'a taşındı, çünkü sys import'u orada daha anlamlı
        self.sys = sys 
        
        self.create_widgets()
        self.refresh_installed_packages()
    
    def setup_theme(self):
        """Modern dark tema ayarları"""
        style = ttk.Style(self.root) 
        style.theme_use('clam')
        
        # Ana renkler
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        accent_color = self.accent_color # Örnek değişkeninden alındı
        
        # Treeview stili
        style.configure('Treeview', 
                       background='#404040',
                       foreground=fg_color,
                       rowheight=25,
                       fieldbackground='#404040')
        style.map('Treeview', background=[('selected', accent_color)])
        style.configure('Treeview.Heading', background=bg_color, foreground=fg_color, font=('Segoe UI', 10, 'bold'))
        
        # Button stili
        style.configure('Modern.TButton',
                       background=accent_color,
                       foreground=fg_color,
                       padding=(10, 5),
                       font=('Segoe UI', 9))
        style.map('Modern.TButton',
                 background=[('active', '#106ebe'),
                           ('pressed', '#005a9e')])
        
        # Entry stili
        style.configure('Modern.TEntry',
                       fieldbackground='#404040',
                       foreground=fg_color,
                       insertcolor=fg_color, # Metin giriş imleci rengi
                       borderwidth=1)
        
        # Frame stili
        style.configure('Modern.TFrame', background=bg_color)

        style.configure('TLabelFrame',
                        background=bg_color,
                        bordercolor=accent_color,
                        relief=tk.SOLID,
                        borderwidth=1
                        )
        style.configure('TLabelFrame.Label',
                        background=bg_color,
                        foreground=fg_color,
                        font=('Segoe UI', 10, 'bold')
                        )

        # Label stili
        style.configure('Modern.TLabel',
                       background=bg_color,
                       foreground=fg_color,
                       font=('Segoe UI', 10))
        
        # Notebook stili
        style.configure('Modern.TNotebook', background=bg_color)
        style.configure('Modern.TNotebook.Tab',
                       background='#404040',
                       foreground=fg_color,
                       padding=[12, 8],
                       font=('Segoe UI', 10))
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', accent_color)],
                 font=[('selected', ('Segoe UI', 10, 'bold'))])
    
    def create_widgets(self):
        """Ana widget'ları oluştur"""
        # Ana container
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Başlık
        title_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        title_frame.pack(fill='x', pady=(0, 10))
        
        title_label = ttk.Label(title_frame, 
                               text="🐍 Modern Python Paket Yöneticisi",
                               style='Modern.TLabel',
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(side='left')
        
        # Durum etiketi
        self.status_label = ttk.Label(title_frame,
                                     text="Hazır",
                                     style='Modern.TLabel',
                                     font=('Segoe UI', 10))
        self.status_label.pack(side='right')
        
        # Notebook (Tab kontrolü)
        self.notebook = ttk.Notebook(main_frame, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Tab'ları oluştur
        ui.create_installed_tab(self)
        ui.create_search_tab(self)
        ui.create_requirements_tab(self)
        ui.create_settings_tab(self)

    def log_message(self, message):
        """Log mesajı ekle"""
        if not hasattr(self, 'log_text') or not self.log_text: 
            print(f"LOG (widget not ready): {message}")
            return

        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.config(state='normal')
        self.log_text.insert('end', log_entry)
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        if self.root and self.root.winfo_exists(): 
            self.root.update_idletasks()
    
    def update_status(self, message):
        """Durum çubuğunu güncelle"""
        if hasattr(self, 'status_label') and self.status_label and self.status_label.winfo_exists():
            self.status_label.config(text=message)
            if self.root and self.root.winfo_exists():
                 self.root.update_idletasks()

    # --- Event Handlers ---
    # Bu metodlar, ilgili handler fonksiyonlarına çağrı yapar.
    # Bu, ana uygulama sınıfını daha temiz tutar.

    def refresh_installed_packages(self): handlers.refresh_installed_packages(self)
    def check_outdated_packages(self): handlers.check_outdated_packages(self)
    def upgrade_selected_installed(self): handlers.upgrade_selected_installed(self)
    def upgrade_all_packages(self): handlers.upgrade_all_packages(self)
    def uninstall_selected(self): handlers.uninstall_selected(self)
    def show_package_details(self): handlers.show_package_details(self)
    def export_package_list(self): handlers.export_package_list(self)
    def filter_installed_packages(self, *args): handlers.filter_installed_packages(self, *args)
    def search_pypi_advanced(self): handlers.search_pypi_advanced(self)
    def install_selected_from_search(self): handlers.install_selected_from_search(self)
    def install_with_options(self): handlers.install_with_options(self)
    def on_search_select(self, event): handlers.on_search_select(self, event)
    def load_requirements(self): handlers.load_requirements(self)
    def save_requirements(self): handlers.save_requirements(self)
    def install_requirements(self): handlers.install_requirements(self)
    def generate_requirements(self): handlers.generate_requirements(self)
    def upgrade_pip(self): handlers.upgrade_pip(self)
    def clear_cache(self): handlers.clear_cache(self)
    def check_broken_packages(self): handlers.check_broken_packages(self)
    def get_selected_package(self, tree): return handlers.get_selected_package(self, tree)
    def run_pip_command(self, command, success_msg="İşlem tamamlandı", show_output=True, callback=None):
        handlers.run_pip_command(self, command, success_msg, show_output, callback)
    def format_size(self, size_bytes): return utils.format_size(size_bytes) 