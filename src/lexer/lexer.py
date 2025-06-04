import re
from enum import Enum, auto

class TokenType(Enum):
    """Vurgulanacak farklı token türleri için Enum"""
    KEYWORD = auto()  # Anahtar Kelime
    OPERATOR = auto()  # Operatör
    IDENTIFIER = auto()  # Tanımlayıcı
    NUMBER = auto()  # Sayı
    STRING = auto()  # Dizi
    COMMENT = auto()  # Yorum
    WHITESPACE = auto()  # Boşluk
    ERROR = auto()  # Hata

class Token:
    """Token bilgilerini saklamak için Token sınıfı"""
    def __init__(self, token_type, value, position):
        self.type = token_type  # Token türü
        self.value = value  # Token değeri
        self.position = position  # (başlangıç, bitiş) çifti

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.position})"

class Lexer:
    """Düzenli ifadeler ve tablolar kullanan sözcüksel analizci uygulaması"""
    def __init__(self):
        # Düzenli ifade desenleri ve token türleriyle token özelliklerini tanımla
        self.token_specs = [
            ('COMMENT', r'//.*?(?:\n|$)|/\*[\s\S]*?\*/', TokenType.COMMENT),
            ('KEYWORD', r'\b(if|else|while|for|return|int|float|string|void|class|function)\b', TokenType.KEYWORD),
            ('STRING', r'"[^"]*"|\'[^\']*\'', TokenType.STRING),
            ('NUMBER', r'\d+(\.\d+)?', TokenType.NUMBER),
            ('OPERATOR', r'[+\-*/=<>!&|;,.(){}[\]]', TokenType.OPERATOR),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
            ('WHITESPACE', r'\s+', TokenType.WHITESPACE),
        ]
        
        # Düzenli ifade deseni oluştur
        self.regex_str = '|'.join(f'(?P<{name}>{pattern})' for name, pattern, _ in self.token_specs)
        self.regex = re.compile(self.regex_str)
        
        # Grup adlarını token türlerine eşle
        self.group_to_type = {name: token_type for name, _, token_type in self.token_specs}
        
    def tokenize(self, text):
        """Giriş metnini token listesine dönüştür"""
        tokens = []
        position = 0
        
        # Metindeki tüm eşleşmeleri bulmak için finditer kullan
        for match in self.regex.finditer(text):
            # Eğer mevcut konum ile eşleşme başlangıcı arasında boşluk varsa,
            # eşleşmeyen metin için bir hata token'i ekle
            if match.start() > position:
                error_text = text[position:match.start()]
                tokens.append(Token(TokenType.ERROR, error_text, (position, match.start())))
            
            # Hangi token türünün eşleştiğini belirle
            token_type = None
            for group_name, group_value in match.groupdict().items():
                if group_value is not None:
                    token_type = self.group_to_type[group_name]
                    break
            
            # Token oluştur
            value = match.group(0)
            start_pos = match.start()
            end_pos = match.end()
            tokens.append(Token(token_type, value, (start_pos, end_pos)))
            
            # Konumu güncelle
            position = end_pos
        
        # Eğer kalan metin varsa, hata token'i olarak ekle
        if position < len(text):
            error_text = text[position:]
            tokens.append(Token(TokenType.ERROR, error_text, (position, len(text))))
        
        return tokens 