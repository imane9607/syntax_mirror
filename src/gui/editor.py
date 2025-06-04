import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, font
import os

from src.highlighter.highlighter import SyntaxHighlighter

class SyntaxHighlighterGUI:
    """GUI application for Syntax Mirror"""
    def __init__(self, root):
        self.root = root
        self.root.title("Syntax Mirror")
        self.root.geometry("900x600")
        
        # Yazı tipini yapılandır
        default_font = font.nametofont("TkFixedFont")
        default_font.configure(family="Courier New", size=12)
        
        # Vurgulayıcıyı oluştur
        self.highlighter = SyntaxHighlighter()
        
        # Dosya yolu değişkenini oluştur
        self.current_file = None
        
        # GUI bileşenlerini oluştur
        self.create_menu()
        self.create_editor()
        self.create_status_bar()
        
        # İlk güncellemeyi zamanla
        self.update_highlighting()
    
    def create_menu(self):
        """Menü çubuğunu oluştur"""
        menubar = tk.Menu(self.root)
        
        # Dosya menüsü
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Yeni", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Aç", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Kaydet", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Farklı Kaydet", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit, accelerator="Alt+F4")
        menubar.add_cascade(label="Dosya", menu=file_menu)
        
        # Düzenleme menüsü
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Geri Al", command=lambda: self.editor.edit_undo(), accelerator="Ctrl+Z")
        edit_menu.add_command(label="Yinele", command=lambda: self.editor.edit_redo(), accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Kes", command=lambda: self.editor.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        edit_menu.add_command(label="Kopyala", command=lambda: self.editor.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        edit_menu.add_command(label="Yapıştır", command=lambda: self.editor.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        menubar.add_cascade(label="Düzenle", menu=edit_menu)
        
        # Yardım menüsü
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Hakkında", command=self.show_about)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # Klavye kısayolları
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-S>", lambda e: self.save_as_file())
    
    def create_editor(self):
        """Metin editörü bileşenini oluştur"""
        # Editör çerçevesini oluştur
        editor_frame = tk.Frame(self.root)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Satır numaralarıyla kaydırılabilir metin widget'ı oluştur
        self.editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            undo=True,
            font="TkFixedFont"
        )
        self.editor.pack(fill=tk.BOTH, expand=True)
        
        # Olayları bağla
        self.editor.bind("<KeyRelease>", self.on_text_change)
    
    def create_status_bar(self):
        """Alt kısımda durum çubuğunu oluştur"""
        self.status_bar = tk.Label(
            self.root,
            text="Hazır",
            anchor=tk.W,
            bd=1,
            relief=tk.SUNKEN
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_highlighting(self):
        """Editör içeriğine sözdizimi vurgulaması uygula"""
        text_content = self.editor.get("1.0", tk.END)
        self.highlighter.apply_highlighting_to_widget(self.editor, text_content)
        
        # Sonraki güncellemeyi zamanla
        self.root.after(500, self.update_highlighting)
    
    def on_text_change(self, event=None):
        """Metin değişikliği olaylarını işle"""
        # Durum çubuğundaki imleç konumunu güncelle
        cursor_position = self.editor.index(tk.INSERT)
        line, column = cursor_position.split(".")
        self.status_bar.config(text=f"Satır: {line} | Sütun: {column}")
        
    def new_file(self):
        """Yeni dosya oluştur"""
        if self.editor.edit_modified():
            save_prompt = messagebox.askyesnocancel("Değişiklikleri Kaydet", "Mevcut dosyadaki değişiklikleri kaydetmek istiyor musunuz?")
            if save_prompt is None:  # İptal
                return
            elif save_prompt:  # Evet
                self.save_file()
        
        self.editor.delete("1.0", tk.END)
        self.editor.edit_modified(False)
        self.current_file = None
        self.root.title("Gerçek Zamanlı Sözdizimi Vurgulayıcı")
    
    def open_file(self):
        """Dosya aç"""
        if self.editor.edit_modified():
            save_prompt = messagebox.askyesnocancel("Değişiklikleri Kaydet", "Mevcut dosyadaki değişiklikleri kaydetmek istiyor musunuz?")
            if save_prompt is None:  # İptal
                return
            elif save_prompt:  # Evet
                self.save_file()
        
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Metin Dosyaları", "*.txt"),
                ("Python Dosyaları", "*.py"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.editor.delete("1.0", tk.END)
                    self.editor.insert("1.0", content)
                    self.editor.edit_modified(False)
                    self.current_file = file_path
                    self.root.title(f"Gerçek Zamanlı Sözdizimi Vurgulayıcı - {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya açılamadı: {str(e)}")
    
    def save_file(self):
        """Mevcut dosyayı kaydet"""
        if self.current_file:
            try:
                content = self.editor.get("1.0", tk.END)
                with open(self.current_file, "w") as file:
                    file.write(content)
                self.editor.edit_modified(False)
                self.status_bar.config(text=f"Dosya kaydedildi: {self.current_file}")
                return True
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilemedi: {str(e)}")
                return False
        else:
            return self.save_as_file()
    
    def save_as_file(self):
        """Farklı kaydet"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Metin Dosyaları", "*.txt"),
                ("Python Dosyaları", "*.py"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        if file_path:
            self.current_file = file_path
            self.root.title(f"Syntax Mirror - {os.path.basename(file_path)}")
            return self.save_file()
        
        return False
    
    def show_about(self):
        """Hakkında iletisini göster"""
        messagebox.showinfo(
            "About Syntax Mirror",
            "Syntax Mirror - Real-time Syntax Highlighter\n\n"
            "A real-time syntax highlighter that performs lexical analysis "
            "and parsing to provide syntax highlighting.\n\n"
            "Created by Imane Keradi"
        ) 