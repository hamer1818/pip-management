import os
import math

def get_dir_size(start_path='.'):
    """Bir dizinin toplam boyutunu hesaplar."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                try:
                    total_size += os.path.getsize(fp)
                except OSError: 
                    pass 
    return total_size

def format_size(size_bytes):
    """Bayt cinsinden boyutu okunabilir bir formata dönüştürür."""
    if size_bytes == -1 or size_bytes is None: 
        return "Bilinmiyor"
    if not isinstance(size_bytes, (int, float)) or size_bytes < 0: 
            return "Hata"
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    if size_bytes < 1: 
        return f"{size_bytes:.1f} B" 
    
    i = int(math.floor(math.log(size_bytes, 1024)))
    if i >= len(size_name): 
        i = len(size_name) - 1

    p = math.pow(1024, i)
    s = round(size_bytes / p, 1) 
    return f"{s} {size_name[i]}"

def sort_treeview_column(tv, col, reverse, is_size=False):
    """Treeview sütununu sıralar."""
    if is_size:
        def get_size_in_bytes(size_str_val): 
            if not isinstance(size_str_val, str) or size_str_val in ["Bilinmiyor", "Hesaplanıyor...", "Hata", "0 B?", "Hata (show)", "Hata (boyut)"]:
                return -float('inf') if reverse else float('inf') 
            
            parts = size_str_val.split()
            if len(parts) != 2: return -float('inf') if reverse else float('inf')
            
            val_str, unit = parts
            try:
                val = float(val_str)
            except ValueError:
                return -float('inf') if reverse else float('inf')

            unit = unit.upper()
            multipliers = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
            if unit in multipliers:
                return val * multipliers[unit]
            return -float('inf') if reverse else float('inf')

        l = [(get_size_in_bytes(tv.set(k, col)), k) for k in tv.get_children('')]
    else: 
        temp_l = []
        for k in tv.get_children(''):
            val = tv.set(k, col)
            try:
                temp_l.append((float(val), k))
            except (ValueError, TypeError):
                temp_l.append((str(val).lower(), k))
        l = temp_l
    
    l.sort(key=lambda t: t[0], reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: sort_treeview_column(tv, col, not reverse, is_size)) 