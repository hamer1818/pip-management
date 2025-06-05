import tkinter as tk
from tkinter import ttk
from . import utils

def create_installed_tab(app):
    """Yüklü paketler sekmesi"""
    installed_frame = ttk.Frame(app.notebook, style='Modern.TFrame')
    app.notebook.add(installed_frame, text="Yüklü Paketler")
    # Üst kontrol paneli
    control_frame = ttk.Frame(installed_frame, style='Modern.TFrame')
    control_frame.pack(fill='x', pady=(0, 10))
    
    # Arama kutusu
    search_frame = ttk.Frame(control_frame, style='Modern.TFrame')
    search_frame.pack(side='left', fill='x', expand=True)
    
    ttk.Label(search_frame, text="Ara:", style='Modern.TLabel').pack(side='left', padx=(0, 5))
    
    app.search_var = tk.StringVar()
    app.search_var.trace_add('write', app.filter_installed_packages) 
    search_entry = ttk.Entry(search_frame, textvariable=app.search_var, style='Modern.TEntry', width=30)
    search_entry.pack(side='left', padx=(0, 10))
    
    # Butonlar
    button_frame = ttk.Frame(control_frame, style='Modern.TFrame')
    button_frame.pack(side='right')
    
    ttk.Button(button_frame, text="🔄 Yenile", 
                command=app.refresh_installed_packages,
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(button_frame, text="📊 Güncel Kontrolü",
                command=app.check_outdated_packages,
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(button_frame, text="⬆️ Seçili Güncelle",
                command=app.upgrade_selected_installed, 
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(button_frame, text="🚀 Tümünü Güncelle",
                command=app.upgrade_all_packages,
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(button_frame, text="🗑️ Kaldır",
                command=app.uninstall_selected,
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(button_frame, text="ℹ️ Detaylar", 
                command=app.show_package_details,
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(button_frame, text="📤 Dışa Aktar",
                command=app.export_package_list,
                style='Modern.TButton').pack(side='left', padx=2)
    
    # Paket listesi
    list_frame = ttk.Frame(installed_frame, style='Modern.TFrame')
    list_frame.pack(fill='both', expand=True)
    
    columns = ('name', 'version', 'latest', 'status', 'size')
    app.installed_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
    
    # Sütun başlıkları
    app.installed_tree.heading('name', text='Paket Adı', command=lambda: utils.sort_treeview_column(app.installed_tree, 'name', False))
    app.installed_tree.heading('version', text='Mevcut Sürüm', command=lambda: utils.sort_treeview_column(app.installed_tree, 'version', False))
    app.installed_tree.heading('latest', text='Son Sürüm', command=lambda: utils.sort_treeview_column(app.installed_tree, 'latest', False))
    app.installed_tree.heading('status', text='Durum', command=lambda: utils.sort_treeview_column(app.installed_tree, 'status', False))
    app.installed_tree.heading('size', text='Boyut', command=lambda: utils.sort_treeview_column(app.installed_tree, 'size', False, is_size=True)) 
    
    # Sütun genişlikleri
    app.installed_tree.column('name', width=250, anchor='w')
    app.installed_tree.column('version', width=120, anchor='center')
    app.installed_tree.column('latest', width=120, anchor='center')
    app.installed_tree.column('status', width=120, anchor='w')
    app.installed_tree.column('size', width=100, anchor='e')
    
    # Scrollbar
    scrollbar_installed = ttk.Scrollbar(list_frame, orient='vertical', command=app.installed_tree.yview)
    app.installed_tree.configure(yscrollcommand=scrollbar_installed.set)
    
    app.installed_tree.pack(side='left', fill='both', expand=True)
    scrollbar_installed.pack(side='right', fill='y')
    app.installed_tree.bind('<Double-1>', lambda e: app.show_package_details())

def create_search_tab(app):
    """Paket arama sekmesi"""
    search_frame_main = ttk.Frame(app.notebook, style='Modern.TFrame') 
    app.notebook.add(search_frame_main, text="Paket Ara & Yükle")
    
    # Arama kontrolleri
    search_control_frame = ttk.Frame(search_frame_main, style='Modern.TFrame')
    search_control_frame.pack(fill='x', pady=(0, 10))
    
    ttk.Label(search_control_frame, text="PyPI'da Ara:", style='Modern.TLabel').pack(side='left', padx=(0, 5))
    
    app.search_query_var = tk.StringVar()
    search_query_entry = ttk.Entry(search_control_frame, textvariable=app.search_query_var,
                                    style='Modern.TEntry', width=40)
    search_query_entry.pack(side='left', padx=(0, 10))
    search_query_entry.bind('<Return>', lambda e: app.search_pypi_advanced()) 
    
    ttk.Button(search_control_frame, text="🔍 Ara",
                command=app.search_pypi_advanced, 
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(search_control_frame, text="📦 Yükle",
                command=app.install_selected_from_search, 
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(search_control_frame, text="⚙️ Gelişmiş Yükle",
                command=app.install_with_options,
                style='Modern.TButton').pack(side='left', padx=2)
    
    # Arama sonuçları
    search_results_frame = ttk.Frame(search_frame_main, style='Modern.TFrame')
    search_results_frame.pack(fill='both', expand=True)
    
    columns = ('name', 'version', 'description', 'author') 
    app.search_tree = ttk.Treeview(search_results_frame, columns=columns, show='headings', height=15)
    
    app.search_tree.heading('name', text='Paket Adı', command=lambda: utils.sort_treeview_column(app.search_tree, 'name', False))
    app.search_tree.heading('version', text='Sürüm', command=lambda: utils.sort_treeview_column(app.search_tree, 'version', False))
    app.search_tree.heading('description', text='Açıklama', command=lambda: utils.sort_treeview_column(app.search_tree, 'description', False))
    app.search_tree.heading('author', text='Geliştirici', command=lambda: utils.sort_treeview_column(app.search_tree, 'author', False)) 
    
    app.search_tree.column('name', width=200, anchor='w')
    app.search_tree.column('version', width=100, anchor='center')
    app.search_tree.column('description', width=400, anchor='w') 
    app.search_tree.column('author', width=150, anchor='w') 
    
    scrollbar_search = ttk.Scrollbar(search_results_frame, orient='vertical', command=app.search_tree.yview)
    app.search_tree.configure(yscrollcommand=scrollbar_search.set)
    
    app.search_tree.pack(side='left', fill='both', expand=True)
    scrollbar_search.pack(side='right', fill='y')
    
    # Detay paneli
    # Stil 'Modern.LabelFrame' kaldırıldı, çünkü artık global 'TLabelFrame' stilini kullanacak.
    detail_frame = ttk.LabelFrame(search_frame_main, text="Paket Bilgisi (PyPI)") 
    detail_frame.pack(fill='x', pady=(10, 0))
    
    app.detail_text = tk.Text(detail_frame, height=8, bg='#1e1e1e', fg='white',
                                font=('Consolas', 9), wrap='word', relief='flat', borderwidth=0)
    scrollbar_detail = ttk.Scrollbar(detail_frame, orient='vertical', command=app.detail_text.yview)
    app.detail_text.configure(yscrollcommand=scrollbar_detail.set)
    
    app.detail_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
    scrollbar_detail.pack(side='right', fill='y')
    
    app.search_tree.bind('<<TreeviewSelect>>', app.on_search_select) 

def create_requirements_tab(app):
    """Requirements.txt yönetim sekmesi"""
    req_frame = ttk.Frame(app.notebook, style='Modern.TFrame')
    app.notebook.add(req_frame, text="Requirements.txt")
    
    # Kontrol paneli
    req_control_frame = ttk.Frame(req_frame, style='Modern.TFrame')
    req_control_frame.pack(fill='x', pady=(0, 10))
    
    ttk.Button(req_control_frame, text="📄 Aç",
                command=app.load_requirements,
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(req_control_frame, text="💾 Kaydet",
                command=app.save_requirements,
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(req_control_frame, text="📦 Tümünü Yükle",
                command=app.install_requirements,
                style='Modern.TButton').pack(side='left', padx=2)
    
    ttk.Button(req_control_frame, text="📋 Mevcutlardan Oluştur",
                command=app.generate_requirements,
                style='Modern.TButton').pack(side='left', padx=2)
    
    # Metin editörü
    app.req_text = tk.Text(req_frame, bg='#1e1e1e', fg='white', insertbackground='white',
                            font=('Consolas', 10), wrap='none', relief='flat', borderwidth=0)
    
    req_scrollbar_v = ttk.Scrollbar(req_frame, orient='vertical', command=app.req_text.yview)
    req_scrollbar_h = ttk.Scrollbar(req_frame, orient='horizontal', command=app.req_text.xview)
    
    app.req_text.configure(yscrollcommand=req_scrollbar_v.set, xscrollcommand=req_scrollbar_h.set)
    
    req_text_frame = ttk.Frame(req_frame, style='Modern.TFrame') 
    req_text_frame.pack(fill='both', expand=True)

    req_scrollbar_h.pack(side='bottom', fill='x')
    req_scrollbar_v.pack(side='right', fill='y')
    app.req_text.pack(in_=req_text_frame, side='left', fill='both', expand=True)

def create_settings_tab(app):
    """Ayarlar sekmesi"""
    settings_frame = ttk.Frame(app.notebook, style='Modern.TFrame')
    app.notebook.add(settings_frame, text="Ayarlar & Bilgi")
    
    # Python bilgileri
    # Stil 'Modern.LabelFrame' kaldırıldı
    info_frame = ttk.LabelFrame(settings_frame, text="Sistem Bilgileri")
    info_frame.pack(fill='x', padx=10, pady=10)
    
    python_version_full = app.sys.version.split('\n')[0] 
    python_info = f"Python Sürümü: {python_version_full}\nPython Yolu: {app.sys.executable}"
    ttk.Label(info_frame, text=python_info, style='Modern.TLabel', justify='left').pack(anchor='w', padx=10, pady=10)
    
    # Pip bilgileri
    # Stil 'Modern.LabelFrame' kaldırıldı
    pip_frame = ttk.LabelFrame(settings_frame, text="Pip İşlemleri")
    pip_frame.pack(fill='x', padx=10, pady=10)
    
    pip_buttons_frame = ttk.Frame(pip_frame, style='Modern.TFrame')
    pip_buttons_frame.pack(fill='x', padx=10, pady=10)
    
    ttk.Button(pip_buttons_frame, text="Pip'i Güncelle",
                command=app.upgrade_pip,
                style='Modern.TButton').pack(side='left', padx=5)
    
    ttk.Button(pip_buttons_frame, text="Cache Temizle",
                command=app.clear_cache,
                style='Modern.TButton').pack(side='left', padx=5)
    
    ttk.Button(pip_buttons_frame, text="Bozuk Paketleri Onar",
                command=app.check_broken_packages,
                style='Modern.TButton').pack(side='left', padx=5)
    
    # Log alanı
    # Stil 'Modern.LabelFrame' kaldırıldı
    log_frame = ttk.LabelFrame(settings_frame, text="İşlem Logları")
    log_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    app.log_text = tk.Text(log_frame, bg='#1e1e1e', fg='#c0c0c0', insertbackground='white', 
                            font=('Consolas', 9), wrap='word', relief='flat', borderwidth=0, state='disabled') 
    log_scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=app.log_text.yview)
    app.log_text.configure(yscrollcommand=log_scrollbar.set)
    
    app.log_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
    log_scrollbar.pack(side='right', fill='y') 