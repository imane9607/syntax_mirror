import tkinter as tk
from tkinter import font
from typing import List, Dict, Any
from src.lexer.lexer import Lexer, TokenType

class SyntaxHighlighter:
    """Metni token'lara ayıran ve vurgulama kurallarını uygulayan sözdizimi vurgulayıcısı"""
    def __init__(self):
        self.lexer = Lexer()
        
        # Temel yazı tiplerini tanımla
        self.normal_font = None
        self.bold_font = None
        self.italic_font = None
        self.bold_italic_font = None
        
        # Token türünden renk ve stil eşleştirmesini tanımla
        self.highlighting_rules = {
            TokenType.KEYWORD: {"foreground": "#0000FF", "font_style": "bold"},         # Mavi, kalın
            TokenType.OPERATOR: {"foreground": "#FF00FF"},                              # Mor
            TokenType.IDENTIFIER: {"foreground": "#000000"},                            # Siyah
            TokenType.NUMBER: {"foreground": "#008000"},                                # Yeşil
            TokenType.STRING: {"foreground": "#A31515"},                                # Koyu kırmızı
            TokenType.COMMENT: {"foreground": "#008000", "font_style": "italic"},       # Yeşil, italik
            TokenType.ERROR: {"foreground": "#FF0000", "background": "#FFEEEE"},        # Açık kırmızı arka plan üzerinde kırmızı
        }
    
    def highlight(self, text):
        """
        Metni işle ve vurgulama talimatlarının bir listesini döndür
        Her talimat (başlangıç_konumu, bitiş_konumu, biçim_sözlüğü) şeklindedir
        """
        tokens = self.lexer.tokenize(text)
        highlighting = []
        
        for token in tokens:
            # Boşluk token'larını atla
            if token.type == TokenType.WHITESPACE:
                continue
            
            # Bu token türü için vurgulama kuralını al
            format_dict = self.highlighting_rules.get(token.type, {}).copy()
            
            # Vurgulama talimatını ekle
            start_pos, end_pos = token.position
            highlighting.append((start_pos, end_pos, format_dict))
        
        return highlighting
    
    def get_token_at_position(self, text, position):
        """Metindeki belirtilen konumdaki token'i al"""
        tokens = self.lexer.tokenize(text)
        
        for token in tokens:
            start_pos, end_pos = token.position
            if start_pos <= position < end_pos:
                return token
        
        return None
    
    def _setup_fonts(self, text_widget):
        """Mevcut metin widget'ının yazı tipine dayalı olarak yazı tipi nesnelerini başlat"""
        if self.normal_font is None:
            # Mevcut yazı tipini al
            current_font = font.Font(font=text_widget['font'])
            family = current_font.actual('family')
            size = current_font.actual('size')
            
            # Yazı tipi varyantlarını oluştur
            self.normal_font = font.Font(family=family, size=size)
            self.bold_font = font.Font(family=family, size=size, weight="bold")
            self.italic_font = font.Font(family=family, size=size, slant="italic")
            self.bold_italic_font = font.Font(family=family, size=size, weight="bold", slant="italic")
        
    def apply_highlighting_to_widget(self, text_widget, text):
        """Bir tkinter Metin widget'ına vurgulama uygula"""
        # Yazı tipleri başlatılmamışsa ayarla
        self._setup_fonts(text_widget)
        
        # Önceki vurgulamaları temizle
        for tag in text_widget.tag_names():
            if tag != "sel":  # Seçim etiketini kaldırma
                text_widget.tag_remove(tag, "1.0", "end")
            
        # Vurgulama talimatlarını al
        highlighting = self.highlight(text)
        
        # Vurgulamayı uygula
        for start_pos, end_pos, format_dict in highlighting:
            # Karakter konumlarını satır.sütun biçimine dönüştür
            start_line, start_col = self._index_to_line_col(text, start_pos)
            end_line, end_col = self._index_to_line_col(text, end_pos)
            
            # Tkinter indeks biçimine dönüştür
            start_index = f"{start_line+1}.{start_col}"
            end_index = f"{end_line+1}.{end_col}"
            
            # Konuma dayalı benzersiz bir etiket adı oluştur
            tag_name = f"highlight_{start_pos}_{end_pos}"
            
            # Yazı tipi stilini diğer özelliklerden farklı şekilde ele al
            font_style = format_dict.pop("font_style", None)
            if font_style == "bold":
                format_dict["font"] = self.bold_font
            elif font_style == "italic":
                format_dict["font"] = self.italic_font
            elif font_style == "bold_italic":
                format_dict["font"] = self.bold_italic_font
            else:
                format_dict["font"] = self.normal_font
                
            # Etiketi biçim ayarlarıyla yapılandır
            text_widget.tag_configure(tag_name, **format_dict)
            
            # Etiketi uygula
            text_widget.tag_add(tag_name, start_index, end_index)
    
    def _index_to_line_col(self, text, index):
        """Karakter indeksini satır ve sütuna dönüştür"""
        if index >= len(text):
            index = len(text) - 1
            
        lines = text[:index+1].split('\n')
        line_count = len(lines) - 1
        col = len(lines[-1]) - 1
        return line_count, col 