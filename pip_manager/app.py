import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
import sys

from . import ui
from . import handlers
from . import utils

class ModernPipManager:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Modern Python Paket Yöneticisi")
        
        # Ana değişkenler
        self.installed_packages = {}
        self.sys = sys 
        
        self.create_widgets()
        self.refresh_installed_packages()
    
    def create_widgets(self):
        """Ana widget'ları oluştur"""
        # Ana container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)
        
        # Başlık bölümü
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 15))
        
        # Ana başlık
        title_label = ttk.Label(
            header_frame, 
            text="🐍 Modern Python Paket Yöneticisi",
            font=("Segoe UI", 20, "bold"),
            bootstyle="info"
        )
        title_label.pack(side=LEFT)
        
        # Durum etiketi
        self.status_label = ttk.Label(
            header_frame,
            text="Hazır",
            font=("Segoe UI", 11),
            bootstyle="secondary"
        )
        self.status_label.pack(side=RIGHT)
        
        # Notebook (Tab kontrolü) - Modern stil
        self.notebook = ttk.Notebook(main_frame, bootstyle="info")
        self.notebook.pack(fill=BOTH, expand=True)
        
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
        self.log_text.config(state=NORMAL)
        self.log_text.insert(END, log_entry)
        self.log_text.see(END)
        self.log_text.config(state=DISABLED)
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