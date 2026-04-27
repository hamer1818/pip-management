import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from . import utils

def create_installed_tab(app):
    """Yüklü paketler sekmesi"""
    installed_frame = ttk.Frame(app.notebook)
    app.notebook.add(installed_frame, text="📦 Yüklü Paketler")
    
    # Üst kontrol paneli
    control_frame = ttk.Frame(installed_frame)
    control_frame.pack(fill=X, pady=(0, 15))
    
    # Arama bölümü
    search_frame = ttk.Frame(control_frame)
    search_frame.pack(side=LEFT, fill=X, expand=True)
    
    ttk.Label(search_frame, text="🔍 Ara:", font=("Segoe UI", 10)).pack(side=LEFT, padx=(0, 8))
    
    app.search_var = tk.StringVar()
    app.search_var.trace_add('write', app.filter_installed_packages) 
    search_entry = ttk.Entry(
        search_frame, 
        textvariable=app.search_var, 
        width=35,
        font=("Segoe UI", 10)
    )
    search_entry.pack(side=LEFT, padx=(0, 15))
    
    # Butonlar
    button_frame = ttk.Frame(control_frame)
    button_frame.pack(side=RIGHT)
    
    # Buton stilleri ve renkler
    buttons = [
        ("🔄 Yenile", app.refresh_installed_packages, "info"),
        ("📊 Güncel Kontrolü", app.check_outdated_packages, "warning"),
        ("⬆️ Seçili Güncelle", app.upgrade_selected_installed, "success"),
        ("🚀 Tümünü Güncelle", app.upgrade_all_packages, "primary"),
        ("🗑️ Kaldır", app.uninstall_selected, "danger"),
        ("ℹ️ Detaylar", app.show_package_details, "secondary"),
        ("📤 Dışa Aktar", app.export_package_list, "dark"),
    ]
    
    for text, command, style in buttons:
        btn = ttk.Button(
            button_frame, 
            text=text,
            command=command,
            bootstyle=style,
            width=12
        )
        btn.pack(side=LEFT, padx=3)
    
    # Paket listesi container
    list_container = ttk.LabelFrame(installed_frame, text="📋 Yüklü Paketler Listesi", padding=10)
    list_container.pack(fill=BOTH, expand=True)
    
    # Treeview için frame
    tree_frame = ttk.Frame(list_container)
    tree_frame.pack(fill=BOTH, expand=True)
    
    columns = ('name', 'version', 'latest', 'status', 'size')
    app.installed_tree = ttk.Treeview(
        tree_frame, 
        columns=columns, 
        show='headings', 
        height=20,
        selectmode="browse"
    )
    
    # Sütun başlıkları ve ayarları
    headers = {
        'name': ('📦 Paket Adı', 250, 'w'),
        'version': ('📋 Mevcut Sürüm', 130, 'center'),
        'latest': ('🆕 Son Sürüm', 130, 'center'),
        'status': ('🔄 Durum', 120, 'w'),
        'size': ('📏 Boyut', 100, 'e')
    }
    
    for col, (text, width, anchor) in headers.items():
        app.installed_tree.heading(
            col, 
            text=text, 
            command=lambda c=col: utils.sort_treeview_column(
                app.installed_tree, c, False, is_size=(c=='size')
            )
        )
        app.installed_tree.column(col, width=width, anchor=anchor)
    
    # Scrollbar
    scrollbar_installed = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=app.installed_tree.yview)
    app.installed_tree.configure(yscrollcommand=scrollbar_installed.set)
    
    app.installed_tree.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar_installed.pack(side=RIGHT, fill=Y)
    
    # Çift tık olayı
    app.installed_tree.bind('<Double-1>', lambda e: app.show_package_details())

def create_search_tab(app):
    """Paket arama sekmesi"""
    search_frame_main = ttk.Frame(app.notebook) 
    app.notebook.add(search_frame_main, text="🔍 Paket Ara & Yükle")
    
    # Arama kontrolleri
    search_control_frame = ttk.LabelFrame(search_frame_main, text="🌐 PyPI Paket Arama", padding=15)
    search_control_frame.pack(fill=X, pady=(0, 15))
    
    # Arama giriş alanı
    search_input_frame = ttk.Frame(search_control_frame)
    search_input_frame.pack(fill=X, pady=(0, 10))
    
    ttk.Label(search_input_frame, text="🔍 Paket Adı:", font=("Segoe UI", 10)).pack(side=LEFT, padx=(0, 8))
    
    app.search_query_var = tk.StringVar()
    search_query_entry = ttk.Entry(
        search_input_frame, 
        textvariable=app.search_query_var,
        width=50,
        font=("Segoe UI", 11)
    )
    search_query_entry.pack(side=LEFT, padx=(0, 10), fill=X, expand=True)
    search_query_entry.bind('<Return>', lambda e: app.search_pypi_advanced()) 
    
    # Arama butonları
    search_buttons_frame = ttk.Frame(search_control_frame)
    search_buttons_frame.pack(fill=X)
    
    search_buttons = [
        ("🔍 Ara", app.search_pypi_advanced, "info"),
        ("📦 Yükle", app.install_selected_from_search, "success"),
        ("⚙️ Gelişmiş Yükle", app.install_with_options, "warning"),
    ]
    
    for text, command, style in search_buttons:
        btn = ttk.Button(
            search_buttons_frame, 
            text=text,
            command=command,
            bootstyle=style,
            width=15
        )
        btn.pack(side=LEFT, padx=5)
    
    # Arama sonuçları
    results_frame = ttk.LabelFrame(search_frame_main, text="📋 Arama Sonuçları", padding=10)
    results_frame.pack(fill=BOTH, expand=True, pady=(0, 15))
    
    # Treeview için frame
    tree_frame = ttk.Frame(results_frame)
    tree_frame.pack(fill=BOTH, expand=True)
    
    columns = ('name', 'version', 'description', 'author') 
    app.search_tree = ttk.Treeview(
        tree_frame, 
        columns=columns, 
        show='headings', 
        height=15,
        selectmode="browse"
    )
    
    # Sütun başlıkları
    search_headers = {
        'name': ('📦 Paket Adı', 200, 'w'),
        'version': ('📋 Sürüm', 100, 'center'),
        'description': ('📝 Açıklama', 450, 'w'),
        'author': ('👤 Geliştirici', 150, 'w')
    }
    
    for col, (text, width, anchor) in search_headers.items():
        app.search_tree.heading(
            col, 
            text=text, 
            command=lambda c=col: utils.sort_treeview_column(app.search_tree, c, False)
        )
        app.search_tree.column(col, width=width, anchor=anchor)
    
    scrollbar_search = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=app.search_tree.yview)
    app.search_tree.configure(yscrollcommand=scrollbar_search.set)
    
    app.search_tree.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar_search.pack(side=RIGHT, fill=Y)
    
    # Detay paneli
    detail_frame = ttk.LabelFrame(search_frame_main, text="📄 Paket Detay Bilgisi", padding=10)
    detail_frame.pack(fill=X)
    
    detail_text_frame = ttk.Frame(detail_frame)
    detail_text_frame.pack(fill=BOTH, expand=True)
    
    app.detail_text = tk.Text(
        detail_text_frame, 
        height=8, 
        bg='#1a1a1a', 
        fg='#ffffff',
        font=('Consolas', 10), 
        wrap='word', 
        relief='flat', 
        borderwidth=0,
        insertbackground='white'
    )
    scrollbar_detail = ttk.Scrollbar(detail_text_frame, orient=VERTICAL, command=app.detail_text.yview)
    app.detail_text.configure(yscrollcommand=scrollbar_detail.set)
    
    app.detail_text.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar_detail.pack(side=RIGHT, fill=Y)
    
    app.search_tree.bind('<<TreeviewSelect>>', app.on_search_select) 

def create_requirements_tab(app):
    """Requirements.txt yönetim sekmesi"""
    req_frame = ttk.Frame(app.notebook)
    app.notebook.add(req_frame, text="📄 Requirements.txt")
    
    # Kontrol paneli
    req_control_frame = ttk.LabelFrame(req_frame, text="📁 Requirements.txt Yönetimi", padding=15)
    req_control_frame.pack(fill=X, pady=(0, 15))
    
    req_buttons = [
        ("📄 Dosya Aç", app.load_requirements, "info"),
        ("💾 Dosya Kaydet", app.save_requirements, "success"),
        ("📦 Tümünü Yükle", app.install_requirements, "primary"),
        ("📋 Mevcutlardan Oluştur", app.generate_requirements, "warning"),
    ]
    
    for text, command, style in req_buttons:
        btn = ttk.Button(
            req_control_frame, 
            text=text,
            command=command,
            bootstyle=style,
            width=18
        )
        btn.pack(side=LEFT, padx=5)
    
    # Metin editörü container
    editor_frame = ttk.LabelFrame(req_frame, text="✏️ Requirements.txt Editörü", padding=10)
    editor_frame.pack(fill=BOTH, expand=True)
    
    # Metin editörü
    text_frame = ttk.Frame(editor_frame)
    text_frame.pack(fill=BOTH, expand=True)
    
    app.req_text = tk.Text(
        text_frame, 
        bg='#1a1a1a', 
        fg='#ffffff', 
        insertbackground='white',
        font=('Consolas', 11), 
        wrap='none', 
        relief='flat', 
        borderwidth=0,
        selectbackground='#404040'
    )
    
    req_scrollbar_v = ttk.Scrollbar(text_frame, orient=VERTICAL, command=app.req_text.yview)
    req_scrollbar_h = ttk.Scrollbar(text_frame, orient=HORIZONTAL, command=app.req_text.xview)
    
    app.req_text.configure(yscrollcommand=req_scrollbar_v.set, xscrollcommand=req_scrollbar_h.set)
    
    req_scrollbar_h.pack(side=BOTTOM, fill=X)
    req_scrollbar_v.pack(side=RIGHT, fill=Y)
    app.req_text.pack(side=LEFT, fill=BOTH, expand=True)

def create_settings_tab(app):
    """Ayarlar sekmesi"""
    settings_frame = ttk.Frame(app.notebook)
    app.notebook.add(settings_frame, text="⚙️ Ayarlar & Bilgi")
    
    # Sistem bilgileri
    info_frame = ttk.LabelFrame(settings_frame, text="💻 Sistem Bilgileri", padding=15)
    info_frame.pack(fill=X, padx=15, pady=15)
    
    python_version_full = app.sys.version.split('\n')[0] 
    python_info = f"🐍 Python Sürümü: {python_version_full}\n📁 Python Yolu: {app.sys.executable}"
    
    info_label = ttk.Label(
        info_frame, 
        text=python_info, 
        justify=LEFT,
        font=("Consolas", 10)
    )
    info_label.pack(anchor=W)
    
    # Pip işlemleri
    pip_frame = ttk.LabelFrame(settings_frame, text="🛠️ Pip İşlemleri", padding=15)
    pip_frame.pack(fill=X, padx=15, pady=(0, 15))
    
    pip_buttons = [
        ("🔄 Pip'i Güncelle", app.upgrade_pip, "primary"),
        ("🗑️ Cache Temizle", app.clear_cache, "warning"),
        ("🔧 Bozuk Paketleri Onar", app.check_broken_packages, "danger"),
    ]
    
    for text, command, style in pip_buttons:
        btn = ttk.Button(
            pip_frame, 
            text=text,
            command=command,
            bootstyle=style,
            width=20
        )
        btn.pack(side=LEFT, padx=8)
    
    # Log alanı
    log_frame = ttk.LabelFrame(settings_frame, text="📊 İşlem Logları", padding=10)
    log_frame.pack(fill=BOTH, expand=True, padx=15, pady=(0, 15))
    
    log_text_frame = ttk.Frame(log_frame)
    log_text_frame.pack(fill=BOTH, expand=True)
    
    app.log_text = tk.Text(
        log_text_frame, 
        bg='#1a1a1a', 
        fg='#c0c0c0', 
        insertbackground='white', 
        font=('Consolas', 10), 
        wrap='word', 
        relief='flat', 
        borderwidth=0, 
        state=DISABLED,
        selectbackground='#404040'
    ) 
    log_scrollbar = ttk.Scrollbar(log_text_frame, orient=VERTICAL, command=app.log_text.yview)
    app.log_text.configure(yscrollcommand=log_scrollbar.set)
    
    app.log_text.pack(side=LEFT, fill=BOTH, expand=True)
    log_scrollbar.pack(side=RIGHT, fill=Y) 