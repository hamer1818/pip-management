import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import threading
import json
from datetime import datetime
import sys
import os
import urllib.request
import urllib.parse
import urllib.error
from . import utils

def run_pip_command(app, command, success_msg="İşlem tamamlandı", show_output=True, callback=None):
    """Pip komutunu çalıştır ve isteğe bağlı callback çağır."""
    def run_command_thread():
        success = False
        output_data = None
        try:
            app.update_status("İşlem devam ediyor...")
            app.log_message(f"Komut çalıştırılıyor: {' '.join(command)}")
            
            result = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0) 
            output_data = result.stdout if result.stdout else ""
            if result.stderr:
                output_data += ("\nStderr: " + result.stderr)

            if result.returncode != 0:
                error_output = result.stderr.strip() if result.stderr and result.stderr.strip() else result.stdout.strip()
                error_msg_detail = f"Hata ({command[3] if len(command)>3 else 'pip'}): {error_output}"
                app.log_message(error_msg_detail)
                app.update_status("Hata oluştu")
                if app.root.winfo_exists(): 
                        messagebox.showerror("Pip Hatası", error_msg_detail, parent=app.root)
            else:
                if show_output and result.stdout:
                    app.log_message(f"Çıktı: {result.stdout.strip()}")
                app.log_message(success_msg)
                app.update_status("Hazır")
                success = True
            
            if any(cmd_part in command for cmd_part in ['install', 'uninstall', 'upgrade']):
                if app.root.winfo_exists():
                    app.root.after(100, app.refresh_installed_packages) 
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Komut Hatası: {e.stderr if e.stderr else str(e)}"
            app.log_message(error_msg)
            app.update_status("Hata oluştu")
            if app.root.winfo_exists(): messagebox.showerror("Komut Hatası", error_msg, parent=app.root)
        except FileNotFoundError:
            error_msg = f"Hata: Pip veya Python bulunamadı. Lütfen PATH ayarlarınızı kontrol edin."
            app.log_message(error_msg)
            app.update_status("Kritik Hata")
            if app.root.winfo_exists(): messagebox.showerror("Kritik Hata", error_msg, parent=app.root)
        except Exception as e:
            error_msg = f"Beklenmeyen hata ({' '.join(command[:4])}...): {str(e)}"
            app.log_message(error_msg)
            app.update_status("Hata oluştu")
            if app.root.winfo_exists(): messagebox.showerror("Beklenmeyen Hata", error_msg, parent=app.root)
        finally:
            if callback:
                if app.root.winfo_exists():
                    app.root.after(0, lambda: callback(success, output_data))
                else: 
                    callback(success, output_data)

    thread = threading.Thread(target=run_command_thread)
    thread.daemon = True
    thread.start()

def refresh_installed_packages(app):
    """Yüklü paketleri ve boyutlarını yenile"""
    def refresh_thread(): 
        app.update_status("Yüklü paketler listeleniyor...")
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], 
                                    capture_output=True, text=True, check=True, encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            packages_data = json.loads(result.stdout)
            new_installed_packages = {pkg['name']: pkg['version'] for pkg in packages_data}
            
            def update_gui_phase1():
                if not app.installed_tree.winfo_exists(): return 

                app.installed_packages = new_installed_packages
                for item in app.installed_tree.get_children():
                    app.installed_tree.delete(item)
                
                for pkg_name, pkg_version in app.installed_packages.items():
                    app.installed_tree.insert('', 'end', iid=pkg_name, values=(
                        pkg_name, pkg_version, 'Kontrol ediliyor...', 'Yüklü', 'Hesaplanıyor...'
                    ))
                
                app.log_message(f"{len(app.installed_packages)} paket listelendi. Boyutlar hesaplanıyor...")
                app.update_status("Paket boyutları hesaplanıyor...")
                
                thread_calc_sizes = threading.Thread(target=calculate_package_sizes_thread, args=(list(app.installed_packages.keys()),))
                thread_calc_sizes.daemon = True
                thread_calc_sizes.start()

            if app.root.winfo_exists():
                app.root.after(0, update_gui_phase1)

        except subprocess.CalledProcessError as e:
            error_msg = f"Paketler yüklenirken pip hatası: {e.stderr}"
            app.log_message(error_msg)
            app.update_status("Hata oluştu")
            if app.root.winfo_exists(): messagebox.showerror("Pip Hatası", error_msg, parent=app.root)
        except Exception as e:
            error_msg = f"Paketler yüklenirken hata: {str(e)}"
            app.log_message(error_msg)
            app.update_status("Hata oluştu")
            if app.root.winfo_exists(): messagebox.showerror("Genel Hata", error_msg, parent=app.root)

    def calculate_package_sizes_thread(package_names_list):
        for i, name in enumerate(package_names_list):
            if not app.root.winfo_exists(): break 
            size_str = "Bilinmiyor"
            try:
                show_result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'show', '--files', name],
                    capture_output=True, text=True, check=False, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                if show_result.returncode != 0:
                    size_str = "Hata (show)"
                else:
                    base_location = None
                    files_section = False
                    package_files_paths = []
                    for line in show_result.stdout.splitlines():
                        if line.startswith("Location: "):
                            base_location = line.split("Location: ", 1)[1].strip()
                        elif line.startswith("Files:"):
                            files_section = True; continue
                        if files_section and line.strip(): package_files_paths.append(line.strip())
                    
                    total_size_bytes = 0
                    if base_location and package_files_paths:
                        for rel_path in package_files_paths:
                            try:
                                abs_file_path = os.path.normpath(os.path.join(base_location, rel_path))
                                if os.path.exists(abs_file_path) and not os.path.islink(abs_file_path) and os.path.isfile(abs_file_path):
                                    total_size_bytes += os.path.getsize(abs_file_path)
                            except OSError: pass
                        size_str = utils.format_size(total_size_bytes)
                    elif base_location : size_str = "0 B?" 
            except Exception: size_str = "Hata (boyut)"

            def update_gui_size(pkg_name_to_update, final_size_str):
                if app.installed_tree.winfo_exists() and app.installed_tree.exists(pkg_name_to_update):
                    current_values = list(app.installed_tree.item(pkg_name_to_update, 'values'))
                    current_values[4] = final_size_str
                    app.installed_tree.item(pkg_name_to_update, values=tuple(current_values))
            
            if app.root.winfo_exists():
                app.root.after(0, lambda n=name, s=size_str: update_gui_size(n, s))
            
            if (i + 1) % 5 == 0: 
                if app.root.winfo_exists():
                        app.root.after(0, lambda: app.update_status(f"Boyutlar hesaplanıyor... ({i+1}/{len(package_names_list)})"))
        
        if app.root.winfo_exists():
            app.root.after(0, lambda: (app.log_message("Paket boyutları hesaplandı."), app.update_status("Hazır")))
    
    main_refresh_thread = threading.Thread(target=refresh_thread)
    main_refresh_thread.daemon = True
    main_refresh_thread.start()

def filter_installed_packages(app, *args):
    """Yüklü paketleri filtrele (Arama kutusuna göre)"""
    if not hasattr(app, 'installed_tree') or not app.installed_tree.winfo_exists():
        return
    
    search_term = app.search_var.get().lower()
    
    for item_id in app.installed_tree.get_children(''):
        values = app.installed_tree.item(item_id, 'values')
        item_text = values[0].lower()
        if search_term in item_text:
            # Item should be visible, ensure it's not detached
            # This is tricky without knowing what's currently attached/detached.
            # A simpler way is to re-insert all matching items.
            pass # For now, let's try a different approach.
    
    all_items = {item_id: app.installed_tree.item(item_id, 'values') for item_id in app.installed_tree.get_children('')}

    # Clear the treeview
    for item in app.installed_tree.get_children():
        app.installed_tree.delete(item)

    # Re-insert items that match the filter
    for item_id, values in all_items.items():
        if search_term in str(values[0]).lower():
            app.installed_tree.insert('', 'end', iid=item_id, values=values)

def get_selected_package(app, tree):
    """Seçili paketi al (Treeview'den)"""
    if not tree.winfo_exists(): return None
    selection = tree.selection()
    if not selection:
        return None
    
    item = tree.item(selection[0])
    if item and item['values']:
        return item['values'][0] 
    return None

def uninstall_selected(app):
    """Seçili paketi kaldır (Yüklü Paketler sekmesinden)"""
    package_name = get_selected_package(app, app.installed_tree)
    if not package_name:
        messagebox.showwarning("Uyarı", "Kaldırmak için lütfen Yüklü Paketler listesinden bir paket seçin.", parent=app.root)
        return
    
    if messagebox.askyesno("Onay", f"'{package_name}' paketini kaldırmak istediğinizden emin misiniz?", parent=app.root):
        command = [sys.executable, '-m', 'pip', 'uninstall', package_name, '-y']
        run_pip_command(app, command, f"'{package_name}' paketi kaldırıldı")

def upgrade_selected_installed(app): 
    """Seçili paketi güncelle (Yüklü Paketler sekmesinden)"""
    package_name = get_selected_package(app, app.installed_tree)
    if not package_name:
        messagebox.showwarning("Uyarı", "Güncellemek için lütfen Yüklü Paketler listesinden bir paket seçin.", parent=app.root)
        return
    
    command = [sys.executable, '-m', 'pip', 'install', '--upgrade', package_name]
    run_pip_command(app, command, f"'{package_name}' paketi güncelleniyor/güncellendi")

def show_package_details(app):
    """Paket detaylarını göster (Yüklü Paketler sekmesinden)"""
    package_name = get_selected_package(app, app.installed_tree)
    if not package_name:
        messagebox.showwarning("Uyarı", "Detaylarını görmek için lütfen Yüklü Paketler listesinden bir paket seçin.", parent=app.root)
        return
    
    def get_details_thread(): 
        try:
            app.update_status(f"'{package_name}' detayları alınıyor...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'show', package_name], 
                                    capture_output=True, text=True, check=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            app.update_status("Hazır")
            
            def create_detail_window_fn(): 
                if not app.root.winfo_exists(): return

                detail_window = tk.Toplevel(app.root)
                detail_window.title(f"{package_name} - Paket Detayları")
                detail_window.geometry("600x450") 
                detail_window.configure(bg='#2b2b2b')
                detail_window.transient(app.root) 
                detail_window.grab_set() 

                text_widget = tk.Text(detail_window, bg='#1e1e1e', fg='white', insertbackground='white',
                                    font=('Consolas', 10), wrap='word', relief='flat', borderwidth=0)
                scrollbar = ttk.Scrollbar(detail_window, orient=VERTICAL, command=text_widget.yview)
                text_widget.configure(yscrollcommand=scrollbar.set)
                
                text_widget.insert('1.0', result.stdout)
                text_widget.config(state=DISABLED) 
                
                text_widget.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
                scrollbar.pack(side=RIGHT, fill=Y)
            
            if app.root.winfo_exists(): app.root.after(0, create_detail_window_fn)
            
        except subprocess.CalledProcessError as e:
            app.update_status("Hata oluştu")
            if app.root.winfo_exists(): messagebox.showerror("Hata", f"'{package_name}' için detaylar alınamadı: {e.stderr}", parent=app.root)
        except Exception as e:
            app.update_status("Hata oluştu")
            if app.root.winfo_exists(): messagebox.showerror("Hata", f"Detaylar alınırken beklenmeyen hata: {str(e)}", parent=app.root)
    
    thread = threading.Thread(target=get_details_thread)
    thread.daemon = True
    thread.start()

def search_pypi_advanced(app): 
    """PyPI'da gelişmiş paket arama (JSON API ve fallback)"""
    query = app.search_query_var.get().strip() 
    if not query:
        messagebox.showwarning("Uyarı", "Lütfen arama terimi girin", parent=app.root)
        return
    
    def search_thread_fn(): 
        try:
            app.update_status(f"PyPI'da '{query}' aranıyor...")
            if app.detail_text.winfo_exists():
                app.detail_text.config(state=NORMAL)
                app.detail_text.delete('1.0', 'end')
                app.detail_text.insert('1.0', f"'{query}' için PyPI'da arama yapılıyor...\n")
                app.detail_text.config(state=DISABLED)

            if app.search_tree.winfo_exists():
                for item in app.search_tree.get_children():
                    app.search_tree.delete(item)
            
            encoded_query = urllib.parse.quote(query)
            url = f"https://pypi.org/pypi/{encoded_query}/json"
            api_hit = False
            
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    data = json.loads(response.read().decode())
                api_hit = True
                info = data['info']
                if app.search_tree.winfo_exists():
                    app.search_tree.insert('', 'end', iid=info['name'], values=( 
                        info['name'],
                        info['version'],
                        info['summary'] or 'Açıklama yok',
                        info.get('author', 'Bilinmiyor') 
                    ))
                app.log_message(f"'{query}' için PyPI JSON API ile sonuç bulundu: {info['name']}")
                
                if app.detail_text.winfo_exists():
                    app.detail_text.config(state=NORMAL)
                    app.detail_text.delete('1.0', 'end')
                    app.detail_text.insert('1.0', f"Paket: {info['name']} v{info['version']}\n")
                    app.detail_text.insert('end', f"Geliştirici: {info.get('author', 'Bilinmiyor')}\n")
                    app.detail_text.insert('end', f"E-posta: {info.get('author_email', 'Bilinmiyor')}\n")
                    app.detail_text.insert('end', f"Anasayfa: {info.get('home_page', 'Bilinmiyor')}\n")
                    app.detail_text.insert('end', f"Lisans: {info.get('license', 'Bilinmiyor')}\n\n")
                    app.detail_text.insert('end', f"Özet:\n{info['summary']}\n\n")
                    if 'description' in info and info['description']:
                            app.detail_text.insert('end', f"Açıklama:\n{info['description'][:1000]}...\n") 
                    app.detail_text.config(state=DISABLED)

            except urllib.error.HTTPError: 
                app.log_message(f"'{query}' için PyPI JSON API ile direkt eşleşme bulunamadı, 'pip index versions' deneniyor...")
                if app.detail_text.winfo_exists():
                    app.detail_text.config(state=NORMAL)
                    app.detail_text.insert('end', "Direkt eşleşme bulunamadı, alternatif arama deneniyor...\n")
                    app.detail_text.config(state=DISABLED)
            except urllib.error.URLError as e_url: 
                app.log_message(f"PyPI JSON API'ye bağlanırken hata: {e_url}")
                if app.detail_text.winfo_exists():
                    app.detail_text.config(state=NORMAL)
                    app.detail_text.insert('end', f"PyPI'ye bağlanılamadı: {e_url}\nAlternatif arama deneniyor...\n")
                    app.detail_text.config(state=DISABLED)
            except json.JSONDecodeError:
                app.log_message(f"PyPI JSON API'den gelen yanıt çözümlenemedi: {query}")
                if app.detail_text.winfo_exists():
                    app.detail_text.config(state=NORMAL)
                    app.detail_text.insert('end', f"PyPI'den gelen yanıt anlaşılamadı.\nAlternatif arama deneniyor...\n")
                    app.detail_text.config(state=DISABLED)


            if not api_hit or not app.search_tree.get_children(): 
                result = subprocess.run([sys.executable, '-m', 'pip', 'index', 'versions', query], 
                                        capture_output=True, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.strip().splitlines()
                    actual_name_match = lines[0].split('(')[0].strip() if lines else query 
                    
                    versions_line = next((line for line in lines if "Available versions:" in line), None)
                    latest_version = "Bilinmiyor"
                    if versions_line:
                        versions_str = versions_line.split("Available versions:",1)[1].strip()
                        if versions_str: latest_version = versions_str.split(',')[-1].strip()
                    
                    if app.search_tree.winfo_exists():
                        app.search_tree.insert('', 'end', iid=actual_name_match, values=( 
                            actual_name_match, latest_version,
                            'PyPI\'da bulundu (detaylar sınırlı)', 'Bilinmiyor'
                        ))
                    app.log_message(f"'{query}' (pip index ile) PyPI'da bulundu: {actual_name_match} v{latest_version}")
                    if app.detail_text.winfo_exists():
                        app.detail_text.config(state=NORMAL)
                        app.detail_text.insert('end', f"'{actual_name_match}' paketi bulundu (Sürüm: {latest_version}). Daha fazla detay için paketi yükleyin.\n")
                        app.detail_text.config(state=DISABLED)
                elif not app.search_tree.get_children(): 
                    error_detail = result.stderr.strip() if result.stderr else "Paket bulunamadı veya erişim hatası."
                    app.log_message(f"'{query}' için 'pip index versions' ile de sonuç bulunamadı: {error_detail}")
                    if app.detail_text.winfo_exists():
                        app.detail_text.config(state=NORMAL)
                        app.detail_text.insert('end', f"'{query}' için arama sonucu bulunamadı.\n{error_detail}\n")
                        app.detail_text.config(state=DISABLED)
                    if app.root.winfo_exists(): messagebox.showinfo("Sonuç Yok", f"'{query}' için arama sonucu bulunamadı.", parent=app.root)
            
            app.update_status("Hazır")
            
        except Exception as e:
            error_msg = f"Arama hatası: {str(e)}"
            app.log_message(error_msg)
            app.update_status("Hata oluştu")
            if app.detail_text.winfo_exists():
                app.detail_text.config(state=NORMAL)
                app.detail_text.insert('end', f"Arama sırasında bir hata oluştu: {str(e)}\n")
                app.detail_text.config(state=DISABLED)
            if app.root.winfo_exists(): messagebox.showerror("Arama Hatası", error_msg, parent=app.root)
    
    thread = threading.Thread(target=search_thread_fn)
    thread.daemon = True
    thread.start()

def install_selected_from_search(app): 
    """Seçili paketi yükle (Paket Ara sekmesinden)"""
    package_name = get_selected_package(app, app.search_tree)
    if not package_name:
        package_name = app.search_query_var.get().strip()
        if not package_name:
            messagebox.showwarning("Uyarı", "Yüklemek için lütfen listeden bir paket seçin veya arama kutusuna adını yazın.", parent=app.root)
            return
    
    command = [sys.executable, '-m', 'pip', 'install', package_name]
    run_pip_command(app, command, f"'{package_name}' paketi yükleniyor/yüklendi")

def on_search_select(app, event): 
    """Arama sonucunda seçim yapıldığında detayları göster (kısmi)"""
    if not app.search_tree.winfo_exists() or not app.detail_text.winfo_exists(): return

    selected_iid = app.search_tree.selection()
    if not selected_iid: return
    
    item_values = app.search_tree.item(selected_iid[0])['values']
    package_name = item_values[0]

    if item_values and len(item_values) > 2 and "detaylar sınırlı" in item_values[2]:
            app.detail_text.config(state=NORMAL)
            app.detail_text.insert('1.0', f"--- Seçili: {package_name} v{item_values[1]} ---\nBu paket 'pip index' ile bulundu. Tam detaylar için paketi yükleyin.\n\n")
            app.detail_text.config(state=DISABLED)

def load_requirements(app):
    """Requirements.txt dosyası yükle"""
    file_path = filedialog.askopenfilename(
        title="Requirements.txt Dosyası Seç",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        parent=app.root
    )
    
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            if app.req_text.winfo_exists():
                app.req_text.delete('1.0', 'end')
                app.req_text.insert('1.0', content)
            app.log_message(f"Requirements dosyası yüklendi: {file_path}")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya okunamadı: {str(e)}", parent=app.root)

def save_requirements(app):
    """Requirements.txt dosyası kaydet"""
    if not app.req_text.winfo_exists(): return

    file_path = filedialog.asksaveasfilename(
        title="Requirements.txt Kaydet",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        parent=app.root
    )
    
    if file_path:
        try:
            content = app.req_text.get('1.0', 'end-1c') 
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            app.log_message(f"Requirements dosyası kaydedildi: {file_path}")
            messagebox.showinfo("Başarılı", "Dosya başarıyla kaydedildi.", parent=app.root)
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilemedi: {str(e)}", parent=app.root)

def install_requirements(app):
    """Requirements.txt dosyasındaki paketleri yükle"""
    if not app.req_text.winfo_exists(): return
    content = app.req_text.get('1.0', 'end-1c').strip()
    if not content:
        messagebox.showwarning("Uyarı", "Requirements.txt içeriği boş veya sadece boşluk içeriyor.", parent=app.root)
        return
    
    temp_file_path = "temp_requirements_install.txt" 
    try:
        with open(temp_file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        command = [sys.executable, '-m', 'pip', 'install', '-r', temp_file_path]
        run_pip_command(app, command, "Requirements.txt dosyasındaki paketler yükleniyor/yüklendi")
        
    except Exception as e: 
        messagebox.showerror("Hata", f"Requirements yüklenirken bir hata oluştu: {str(e)}", parent=app.root)
        app.log_message(f"Requirements yükleme hatası (dosya işlemi): {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError as e_os:
                app.log_message(f"Geçici requirements dosyası silinemedi: {e_os}")

def generate_requirements(app):
    """Mevcut paketlerden requirements.txt oluştur"""
    def generate_thread_fn(): 
        try:
            app.update_status("Requirements.txt oluşturuluyor...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], 
                                    capture_output=True, text=True, check=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            if app.req_text.winfo_exists():
                app.req_text.delete('1.0', 'end')
                app.req_text.insert('1.0', result.stdout)
            app.log_message("Mevcut paketlerden Requirements.txt oluşturuldu.")
            app.update_status("Hazır")
            
        except subprocess.CalledProcessError as e:
            app.update_status("Hata oluştu")
            if app.root.winfo_exists(): messagebox.showerror("Pip Hatası", f"Requirements oluşturulamadı: {e.stderr}", parent=app.root)
        except Exception as e:
            app.update_status("Hata oluştu")
            if app.root.winfo_exists(): messagebox.showerror("Genel Hata", f"Requirements oluşturulurken beklenmeyen hata: {str(e)}", parent=app.root)
    
    thread = threading.Thread(target=generate_thread_fn)
    thread.daemon = True
    thread.start()

def upgrade_pip(app):
    """Pip'i güncelle"""
    command = [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip']
    run_pip_command(app, command, "Pip başarıyla güncellendi.")

def clear_cache(app):
    """Pip cache'ini temizle"""
    if messagebox.askyesno("Onay", "Pip önbelleğini temizlemek istediğinizden emin misiniz? Bu işlem geri alınamaz.", parent=app.root):
        command = [sys.executable, '-m', 'pip', 'cache', 'purge']
        run_pip_command(app, command, "Pip önbelleği temizlendi.")

def check_broken_packages(app):
    """Bozuk paketleri kontrol et"""
    def check_thread_fn(): 
        try:
            app.update_status("Bozuk paketler kontrol ediliyor...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'check'], 
                                    capture_output=True, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0) 
            
            output = result.stdout.strip() if result.stdout else ""
            if result.stderr and result.stderr.strip(): 
                output += f"\nStderr: {result.stderr.strip()}"

            app.log_message(f"Pip check sonucu:\n{output if output else 'Çıktı yok'}")

            if not app.root.winfo_exists(): return 

            if result.returncode == 0 or "No broken requirements found." in output:
                messagebox.showinfo("Sonuç", "Bozuk veya uyumsuz paket bulunamadı.", parent=app.root)
            else: 
                messagebox.showwarning("Uyarı", f"Bozuk veya uyumsuz paketler bulundu:\n\n{output}", parent=app.root)
            
            app.update_status("Hazır")
            
        except Exception as e:
            error_msg = f"Paket kontrolü sırasında hata: {str(e)}"
            app.log_message(error_msg)
            if app.root.winfo_exists(): messagebox.showerror("Hata", error_msg, parent=app.root)
            app.update_status("Hata oluştu")
    
    thread = threading.Thread(target=check_thread_fn)
    thread.daemon = True
    thread.start()

def check_outdated_packages(app):
    """Güncellenebilir paketleri kontrol et"""
    def check_outdated_thread_fn(): 
        try:
            app.update_status("Güncel olmayan paketler kontrol ediliyor...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'], 
                                    capture_output=True, text=True, check=False, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0) 
            
            if not app.root.winfo_exists(): return 

            if result.returncode != 0: 
                app.log_message(f"Güncel olmayan paketler kontrol edilirken hata: {result.stderr}")
                messagebox.showerror("Hata", f"Güncel olmayan paketler listelenemedi: {result.stderr}", parent=app.root)
                app.update_status("Hata oluştu")
                return

            outdated_packages_data = [] 
            if result.stdout.strip(): 
                try:
                    outdated_packages_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    app.log_message(f"Güncel olmayan paket listesi JSON formatında değil: {result.stdout[:200]}")
                    messagebox.showerror("Hata", "Güncel olmayan paket listesi alınamadı (format hatası).", parent=app.root)
                    app.update_status("Hata oluştu")
                    return
            
            if not app.installed_tree.winfo_exists(): return 

            for item_id in app.installed_tree.get_children():
                values = list(app.installed_tree.item(item_id)['values'])
                package_name = values[0]
                is_outdated_flag = False 
                
                for pkg_info in outdated_packages_data:
                    if pkg_info['name'] == package_name:
                        values[2] = pkg_info['latest_version']  
                        values[3] = 'Güncellenebilir'  
                        app.installed_tree.item(item_id, values=tuple(values))
                        is_outdated_flag = True
                        break
                
                if not is_outdated_flag: 
                    if values[2] == 'Kontrol ediliyor...' or values[3] != 'Güncel': 
                            values[2] = values[1]  
                            values[3] = 'Güncel'
                            app.installed_tree.item(item_id, values=tuple(values))
            
            if outdated_packages_data:
                app.log_message(f"{len(outdated_packages_data)} güncellenebilir paket bulundu.")
                messagebox.showinfo("Sonuç", f"{len(outdated_packages_data)} adet güncellenebilir paket bulundu.", parent=app.root)
            else:
                app.log_message("Tüm yüklü paketler güncel.")
                messagebox.showinfo("Sonuç", "Tüm yüklü paketler güncel görünüyor.", parent=app.root)
            
            app.update_status("Hazır")
            
        except Exception as e:
            error_msg = f"Güncel paket kontrolü sırasında hata: {str(e)}"
            app.log_message(error_msg)
            if app.root.winfo_exists(): messagebox.showerror("Hata", error_msg, parent=app.root)
            app.update_status("Hata oluştu")
    
    thread = threading.Thread(target=check_outdated_thread_fn)
    thread.daemon = True
    thread.start()

def upgrade_all_packages(app):
    """Tüm güncellenebilir paketleri güncelle"""
    def upgrade_all_thread_fn(): 
        try:
            app.update_status("Güncellenebilir paketler bulunuyor...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'], 
                                    capture_output=True, text=True, check=False, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            if not app.root.winfo_exists(): return

            if result.returncode != 0:
                app.log_message(f"Toplu güncelleme için paketler listelenemedi: {result.stderr}")
                messagebox.showerror("Hata", f"Güncellenecek paketler listelenemedi: {result.stderr}", parent=app.root)
                app.update_status("Hata oluştu")
                return

            outdated_packages_list = [] 
            if result.stdout.strip():
                try:
                    outdated_packages_list = json.loads(result.stdout)
                except json.JSONDecodeError:
                    app.log_message(f"Güncel olmayan paket listesi (toplu güncelleme) JSON formatında değil: {result.stdout[:200]}")
                    messagebox.showerror("Hata", "Güncellenecek paket listesi alınamadı (format hatası).", parent=app.root)
                    app.update_status("Hata oluştu")
                    return

            if not outdated_packages_list:
                messagebox.showinfo("Bilgi", "Güncellenecek paket bulunamadı.", parent=app.root)
                app.update_status("Hazır")
                return
            
            package_names_list = [pkg['name'] for pkg in outdated_packages_list] 
            confirm_msg = f"{len(package_names_list)} paket güncellenecek:\n" + ", ".join(package_names_list[:5])
            if len(package_names_list) > 5:
                confirm_msg += f"\n... ve {len(package_names_list) - 5} paket daha."
            
            if not messagebox.askyesno("Onay", confirm_msg + "\n\nTümünü güncellemek istediğinizden emin misiniz?", parent=app.root):
                app.update_status("Hazır")
                return
            
            app.log_message(f"Toplu güncelleme başlatılıyor: {len(outdated_packages_list)} paket.")
            for i, package_info in enumerate(outdated_packages_list):
                if not app.root.winfo_exists(): break 
                package_name = package_info['name']
                app.update_status(f"Güncelleniyor: {package_name} ({i+1}/{len(outdated_packages_list)})")
                upgrade_cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade', package_name]
                run_pip_command(app, upgrade_cmd, f"'{package_name}' güncelleme komutu gönderildi.", show_output=False)
            
            app.log_message(f"Tüm güncellenebilir paketler için güncelleme komutları gönderildi. Yenileme bekleniyor...")
            if app.root.winfo_exists():
                app.root.after(3000, app.refresh_installed_packages) 
            app.update_status("Toplu güncelleme komutları gönderildi.")
            
        except Exception as e:
            error_msg = f"Toplu güncelleme sırasında hata: {str(e)}"
            app.log_message(error_msg)
            if app.root.winfo_exists(): messagebox.showerror("Hata", error_msg, parent=app.root)
            app.update_status("Hata oluştu")
    
    thread = threading.Thread(target=upgrade_all_thread_fn)
    thread.daemon = True
    thread.start()

def export_package_list(app):
    """Paket listesini dışa aktar"""
    if not app.installed_packages: 
        messagebox.showwarning("Uyarı", "Dışa aktarılacak yüklü paket bulunmuyor. Lütfen önce listeyi yenileyin.", parent=app.root)
        return
    
    file_path = filedialog.asksaveasfilename(
        title="Paket Listesini Kaydet",
        defaultextension=".txt",
        filetypes=[
            ("Text files (requirements format)", "*.txt"),
            ("JSON files", "*.json"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ],
        parent=app.root
    )
    
    if file_path:
        try:
            freeze_result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], 
                                            capture_output=True, text=True, check=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            current_pkgs_freeze_list = freeze_result.stdout.strip().splitlines() 
            
            current_pkgs_dict = {} 
            for line in current_pkgs_freeze_list:
                if '==' in line:
                    name, version = line.split('==', 1)
                    current_pkgs_dict[name] = version

            if file_path.endswith('.json'):
                export_data = {
                    'export_date': datetime.now().isoformat(),
                    'python_version': sys.version.split('\n')[0],
                    'packages': current_pkgs_dict
                }
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(export_data, file, indent=2, ensure_ascii=False)
            
            elif file_path.endswith('.csv'):
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write("Package Name,Version\n")
                    for name, version in sorted(current_pkgs_dict.items()):
                        file.write(f"{name},{version}\n")
            
            else: 
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(f"# Python Paket Listesi (requirements.txt formatında)\n")
                    file.write(f"# Dışa Aktarma Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write(f"# Python Sürümü: {sys.version.splitlines()[0]}\n")
                    file.write(f"# Toplam Paket Sayısı: {len(current_pkgs_freeze_list)}\n")
                    file.write(f"# {'-'*50}\n\n")
                    file.write(freeze_result.stdout) 
            
            app.log_message(f"Paket listesi dışa aktarıldı: {file_path}")
            messagebox.showinfo("Başarılı", f"Paket listesi başarıyla kaydedildi:\n{file_path}", parent=app.root)
        except subprocess.CalledProcessError as e:
            error_msg = f"Dışa aktarma için paket listesi alınamadı (pip freeze hatası): {e.stderr}"
            app.log_message(error_msg)
            if app.root.winfo_exists(): messagebox.showerror("Pip Hatası", error_msg, parent=app.root)
        except Exception as e:
            error_msg = f"Dışa aktarma sırasında hata: {str(e)}"
            app.log_message(error_msg)
            if app.root.winfo_exists(): messagebox.showerror("Dosya Hatası", error_msg, parent=app.root)

def install_with_options(app):
    """Gelişmiş kurulum seçenekleri ile paket kur"""
    selected_pkg_name_options = get_selected_package(app, app.search_tree) 
    if not selected_pkg_name_options:
        selected_pkg_name_options = app.search_query_var.get().strip()
        if not selected_pkg_name_options:
            messagebox.showwarning("Uyarı", "Kurmak için lütfen listeden bir paket seçin veya arama kutusuna adını yazın.", parent=app.root)
            return
    
    options_window = tk.Toplevel(app.root)
    options_window.title(f"'{selected_pkg_name_options}' Kurulum Seçenekleri")
    options_window.geometry("450x400") 
    options_window.resizable(False, False)
    options_window.transient(app.root)
    options_window.grab_set()
    options_window.configure(bg='#2b2b2b') 

    app.root.update_idletasks() 
    options_window.update_idletasks() 
    
    root_x, root_y = app.root.winfo_x(), app.root.winfo_y()
    root_width, root_height = app.root.winfo_width(), app.root.winfo_height()
    win_width, win_height = options_window.winfo_width(), options_window.winfo_height()
    
    x_coord = root_x + (root_width // 2) - (win_width // 2) 
    y_coord = root_y + (root_height // 2) - (win_height // 2) 
    options_window.geometry(f"{win_width}x{win_height}+{x_coord}+{y_coord}")
    
    s_options = ttk.Style(options_window) 
    s_options.configure('Options.TLabel', background='#2b2b2b', foreground='white', font=('Segoe UI', 10))
    s_options.configure('Options.TCheckbutton', background='#2b2b2b', foreground='white', font=('Segoe UI', 9)) 
    s_options.map('Options.TCheckbutton',
            background=[('active', '#404040')])

    s_options.configure('Options.TEntry', fieldbackground='#404040', foreground='white', insertcolor='white')
    s_options.configure('Options.TButton', background='#0078d4', foreground='white', padding=(8,4), font=('Segoe UI', 9))
    s_options.map('Options.TButton', background=[('active', '#106ebe')])


    ttk.Label(options_window, text=f"Paket: {selected_pkg_name_options}", font=('Segoe UI', 12, 'bold'), style='Options.TLabel').pack(pady=10)
    
    options_frame_inner = ttk.Frame(options_window, style='Modern.TFrame', padding=(10,5)) 
    options_frame_inner.pack(padx=20, pady=5, fill='both', expand=True)
    
    upgrade_var_opt = tk.BooleanVar() 
    user_var_opt = tk.BooleanVar() 
    no_deps_var_opt = tk.BooleanVar() 
    force_var_opt = tk.BooleanVar() 
    no_cache_var_opt = tk.BooleanVar() 
    
    ttk.Checkbutton(options_frame_inner, text="Mevcut paketi güncelle (--upgrade)", variable=upgrade_var_opt, style='Options.TCheckbutton').pack(anchor='w', pady=3)
    ttk.Checkbutton(options_frame_inner, text="Kullanıcı dizinine kur (--user)", variable=user_var_opt, style='Options.TCheckbutton').pack(anchor='w', pady=3)
    ttk.Checkbutton(options_frame_inner, text="Bağımlılıkları kurma (--no-deps)", variable=no_deps_var_opt, style='Options.TCheckbutton').pack(anchor='w', pady=3)
    ttk.Checkbutton(options_frame_inner, text="Zorla yeniden kur (--force-reinstall)", variable=force_var_opt, style='Options.TCheckbutton').pack(anchor='w', pady=3)
    ttk.Checkbutton(options_frame_inner, text="Önbelleği kullanma (--no-cache-dir)", variable=no_cache_var_opt, style='Options.TCheckbutton').pack(anchor='w', pady=3)
    
    ttk.Label(options_frame_inner, text="Belirli sürüm (isteğe bağlı):", style='Options.TLabel').pack(anchor='w', pady=(10, 2))
    version_entry_opt = ttk.Entry(options_frame_inner, width=30, style='Options.TEntry') 
    version_entry_opt.pack(anchor='w', padx=10, fill='x')
    ttk.Label(options_frame_inner, text="Örnek: ==1.2.3, >=1.0, <2.0", font=('Segoe UI', 8), style='Options.TLabel', foreground='gray').pack(anchor='w', padx=10)
    
    button_frame_opt = ttk.Frame(options_window, style='Modern.TFrame') 
    button_frame_opt.pack(pady=15, fill='x', padx=20)
    
    def do_install_package_fn(): 
        try:
            cmd_list = [sys.executable, '-m', 'pip', 'install'] 
            
            if upgrade_var_opt.get(): cmd_list.append('--upgrade')
            if user_var_opt.get(): cmd_list.append('--user')
            if no_deps_var_opt.get(): cmd_list.append('--no-deps')
            if force_var_opt.get(): cmd_list.append('--force-reinstall')
            if no_cache_var_opt.get(): cmd_list.append('--no-cache-dir')
            
            package_spec_final = selected_pkg_name_options 
            version_spec_str = version_entry_opt.get().strip() 
            if version_spec_str:
                if not (version_spec_str.startswith('==') or version_spec_str.startswith('>=') or \
                        version_spec_str.startswith('<=') or version_spec_str.startswith('!=') or \
                        version_spec_str.startswith('~=') or version_spec_str.startswith('<') or \
                        version_spec_str.startswith('>')):
                    messagebox.showwarning("Geçersiz Sürüm", "Sürüm belirteci geçersiz. Örnek: ==1.2.3, >=1.0", parent=options_window)
                    return
                package_spec_final += version_spec_str
            
            cmd_list.append(package_spec_final)
            
            if options_window.winfo_exists(): options_window.destroy() 
            run_pip_command(app, cmd_list, f"'{package_spec_final}' paketi için kurulum komutu gönderildi.")
            
        except Exception as e_install_opt: 
            error_msg = f"Kurulum seçenekleri hazırlanırken hata: {str(e_install_opt)}"
            app.log_message(error_msg)
            parent_win = options_window if options_window.winfo_exists() else app.root
            messagebox.showerror("Seçenek Hatası", error_msg, parent=parent_win)
    
    ttk.Button(button_frame_opt, text="Kur", command=do_install_package_fn, style='Options.TButton').pack(side=RIGHT, padx=5) 
    ttk.Button(button_frame_opt, text="İptal", command=options_window.destroy, style='Options.TButton').pack(side=RIGHT, padx=5) 