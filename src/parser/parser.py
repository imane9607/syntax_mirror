from typing import List, Tuple, Optional
from src.lexer.lexer import Token, TokenType

class ASTNode:
    """Soyut Sözdizimi Ağacı (AST) düğümleri için temel sınıf"""
    def __init__(self, node_type, children=None):
        self.type = node_type
        self.children = children or []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __str__(self):
        return f"{self.type}({', '.join(str(child) for child in self.children)})"

class Parser:
    """Yukarıdan aşağıya özyinelemeli iniş ayrıştırıcı uygulaması"""
    def __init__(self, tokens=None):
        self.tokens = tokens or []
        self.current_token_index = 0
        self.errors = []
    
    def set_tokens(self, tokens):
        """Ayrıştırılacak token'ları ayarla"""
        self.tokens = tokens
        self.current_token_index = 0
        self.errors = []
    
    def peek(self):
        """Tüketmeden mevcut token'a bak"""
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None
    
    def consume(self):
        """Mevcut token'ı tüket ve bir sonrakine ilerle"""
        if self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            self.current_token_index += 1
            return token
        return None
    
    def match(self, token_type):
        """Mevcut token'in beklenen türe uyup uymadığını kontrol et ve tüket"""
        if self.peek() and self.peek().type == token_type:
            return self.consume()
        return None
    
    def expect(self, token_type, error_message):
        """Belirli bir türde token bekle, bulunamazsa hata oluştur"""
        token = self.match(token_type)
        if not token:
            self.errors.append(error_message)
        return token
    
    def parse(self) -> Tuple[ASTNode, List[str]]:
        """Token'ları soyut sözdizimi ağacına ayrıştır"""
        # Bu, yalnızca token dizisini doğrulayan basitleştirilmiş bir ayrıştırıcıdır
        # Gerçek bir ayrıştırıcı için, dilbilgisindeki her bir terminal olmayan için
        # üretim kurallarını uygulayan yöntemleriniz olurdu
        
        # Basit bir dil için örnek dilbilgisi kuralları şu şekilde olabilir:
        # program -> ifade*
        # ifade -> ifade_cümlesi | tanımlama | if_cümlesi | while_cümlesi
        # ifade_cümlesi -> ifade ';'
        # tanımlama -> tür tanımlayıcı ('=' ifade)? ';'
        # vb.
        
        root = ASTNode("Program")
        
        while self.peek() and self.peek().type != TokenType.ERROR:
            # Boşlukları veya yorumları atla
            while self.peek() and self.peek().type in (TokenType.WHITESPACE, TokenType.COMMENT):
                self.consume()
            
            # Başka token kalmadıysa veya sadece boşluk/yorum kaldıysa, işimiz bitti
            if not self.peek() or self.peek().type == TokenType.ERROR:
                break
            
            # Bir ifadeyi ayrıştır (bu basitleştirilmiş bir örnektir)
            statement = self.parse_statement()
            if statement:
                root.add_child(statement)
        
        return root, self.errors
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Dilbilgisine göre bir ifadeyi ayrıştır"""
        # Bu basitleştirilmiş bir sürümdür - gerçek bir ayrıştırıcıda 
        # her ifade türü için özel yöntemler olurdu
        
        token = self.peek()
        
        if not token:
            return None
            
        # İlk token'a dayalı olarak ifade türlerinin basit tanımlanması
        if token.type == TokenType.KEYWORD:
            if token.value == "if":
                return self.parse_if_statement()
            elif token.value == "while":
                return self.parse_while_statement()
            elif token.value in ("int", "float", "string", "void"):
                return self.parse_declaration()
            elif token.value == "return":
                return self.parse_return_statement()
        
        # Varsayılan olarak ifade cümlesi
        return self.parse_expression_statement()
    
    def parse_if_statement(self) -> ASTNode:
        """Bir if ifadesini ayrıştır"""
        # Basitleştirilmiş uygulama
        self.consume()  # 'if' token'ını tüket
        node = ASTNode("IfStatement")
        return node
    
    def parse_while_statement(self) -> ASTNode:
        """Bir while ifadesini ayrıştır"""
        # Basitleştirilmiş uygulama
        self.consume()  # 'while' token'ını tüket
        node = ASTNode("WhileStatement")
        return node
        
    def parse_declaration(self) -> ASTNode:
        """Bir değişken veya fonksiyon tanımlamasını ayrıştır"""
        # Basitleştirilmiş uygulama
        type_token = self.consume()
        node = ASTNode("Declaration", [type_token.value])
        return node
    
    def parse_return_statement(self) -> ASTNode:
        """Bir return ifadesini ayrıştır"""
        # Basitleştirilmiş uygulama
        self.consume()  # 'return' token'ını tüket
        node = ASTNode("ReturnStatement")
        return node
    
    def parse_expression_statement(self) -> ASTNode:
        """Bir ifade cümlesini ayrıştır"""
        # Basitleştirilmiş uygulama
        # Gerçek bir ayrıştırıcıda, bu işlem operatör önceliğine göre ifadeleri ayrıştırmayı
        # ve uygun bir ifade ağacı oluşturmayı içerirdi
        
        # Basitlik için, sadece noktalı virgül bulana kadar token'ları tüketeceğiz
        node = ASTNode("ExpressionStatement")
        return node

    def program(self) -> ASTNode:
        """Program -> İfade*"""
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return ASTNode("Program", children=statements)
    
    def statement(self) -> ASTNode:
        """Parse a statement"""
        if self.match(TokenType.KEYWORD):
            return self.keyword_statement()
        return self.expression()
    
    def keyword_statement(self) -> ASTNode:
        """Parse a keyword statement (if, while, etc.)"""
        keyword = self.previous()
        if keyword.value == "if":
            return self.if_statement()
        elif keyword.value in ("while", "for"):
            return self.loop_statement()
        elif keyword.value == "def":
            return self.function_definition()
        elif keyword.value == "class":
            return self.class_definition()
        elif keyword.value == "return":
            return self.return_statement()
        else:
            return self.expression()
    
    def function_definition(self) -> ASTNode:
        """Parse a function definition"""
        # Consume 'def' keyword
        self.consume()
        
        # Get function name
        name = self.consume()
        
        # Parse parameters
        self.consume()  # '('
        parameters = []
        if not self.check(TokenType.OPERATOR) or self.peek().value != ")":
            parameters.append(self.parameter())
            while self.match(TokenType.OPERATOR) and self.previous().value == ",":
                parameters.append(self.parameter())
        self.consume()  # ')'
        
        # Parse function body
        self.consume()  # ':'
        body = []
        while not self.is_at_end() and not self.check(TokenType.KEYWORD):
            body.append(self.statement())
        
        return ASTNode("Function", children=[
            ASTNode("Parameters", children=parameters),
            ASTNode("Body", children=body)
        ])
    
    def parameter(self) -> ASTNode:
        """Parse a function parameter"""
        name = self.consume()
        return ASTNode("Parameter", name.value)
    
    def if_statement(self) -> ASTNode:
        """Parse an if statement"""
        # Consume 'if' keyword
        self.consume()
        
        # Parse condition
        condition = self.expression()
        
        # Parse body
        self.consume()  # ':'
        body = []
        while not self.is_at_end() and not self.check(TokenType.KEYWORD):
            body.append(self.statement())
        
        return ASTNode("If", children=[
            ASTNode("Condition", children=[condition]),
            ASTNode("Body", children=body)
        ])
    
    def loop_statement(self) -> ASTNode:
        """Parse a while or for loop"""
        keyword = self.previous()
        
        if keyword.value == "while":
            # Parse while loop
            condition = self.expression()
            self.consume()  # ':'
            body = []
            while not self.is_at_end() and not self.check(TokenType.KEYWORD):
                body.append(self.statement())
            return ASTNode("While", children=[
                ASTNode("Condition", children=[condition]),
                ASTNode("Body", children=body)
            ])
        else:
            # Parse for loop
            target = self.consume()
            self.consume()  # 'in'
            iterable = self.expression()
            self.consume()  # ':'
            body = []
            while not self.is_at_end() and not self.check(TokenType.KEYWORD):
                body.append(self.statement())
            return ASTNode("For", children=[
                ASTNode("Target", target.value),
                ASTNode("Iterable", children=[iterable]),
                ASTNode("Body", children=body)
            ])
    
    def class_definition(self) -> ASTNode:
        """Parse a class definition"""
        # Consume 'class' keyword
        self.consume()
        
        # Get class name
        name = self.consume()
        
        # Parse class body
        self.consume()  # ':'
        body = []
        while not self.is_at_end() and not self.check(TokenType.KEYWORD):
            body.append(self.statement())
        
        return ASTNode("Class", name.value, body)
    
    def return_statement(self) -> ASTNode:
        """Parse a return statement"""
        # Consume 'return' keyword
        self.consume()
        
        # Parse return value
        value = self.expression()
        return ASTNode("Return", children=[value])
    
    def expression(self) -> ASTNode:
        """Parse an expression"""
        return self.assignment()
    
    def assignment(self) -> ASTNode:
        """Parse an assignment expression"""
        expr = self.equality()
        
        if self.match(TokenType.OPERATOR) and self.previous().value == "=":
            value = self.assignment()
            return ASTNode("Assignment", children=[expr, value])
        
        return expr
    
    def equality(self) -> ASTNode:
        """Parse equality expressions"""
        expr = self.comparison()
        
        while self.match(TokenType.OPERATOR) and self.previous().value in ("==", "!="):
            operator = self.previous().value
            right = self.comparison()
            expr = ASTNode("Binary", operator, [expr, right])
        
        return expr
    
    def comparison(self) -> ASTNode:
        """Parse comparison expressions"""
        expr = self.term()
        
        while self.match(TokenType.OPERATOR) and self.previous().value in ("<", ">", "<=", ">="):
            operator = self.previous().value
            right = self.term()
            expr = ASTNode("Binary", operator, [expr, right])
        
        return expr
    
    def term(self) -> ASTNode:
        """Parse addition/subtraction"""
        expr = self.factor()
        
        while self.match(TokenType.OPERATOR) and self.previous().value in ("+", "-"):
            operator = self.previous().value
            right = self.factor()
            expr = ASTNode("Binary", operator, [expr, right])
        
        return expr
    
    def factor(self) -> ASTNode:
        """Parse multiplication/division"""
        expr = self.unary()
        
        while self.match(TokenType.OPERATOR) and self.previous().value in ("*", "/"):
            operator = self.previous().value
            right = self.unary()
            expr = ASTNode("Binary", operator, [expr, right])
        
        return expr
    
    def unary(self) -> ASTNode:
        """Parse unary expressions"""
        if self.match(TokenType.OPERATOR) and self.previous().value in ("-", "not"):
            operator = self.previous().value
            right = self.unary()
            return ASTNode("Unary", operator, [right])
        
        return self.primary()
    
    def primary(self) -> ASTNode:
        """Parse primary expressions"""
        if self.match(TokenType.NUMBER):
            return ASTNode("Number", self.previous().value)
        elif self.match(TokenType.STRING):
            return ASTNode("String", self.previous().value)
        elif self.match(TokenType.IDENTIFIER):
            return ASTNode("Identifier", self.previous().value)
        elif self.match(TokenType.KEYWORD) and self.previous().value in ("True", "False", "None"):
            return ASTNode("Literal", self.previous().value)
        
        # Handle parentheses
        if self.match(TokenType.OPERATOR) and self.previous().value == "(":
            expr = self.expression()
            self.consume()  # ')'
            return expr
        
        return ASTNode("Error")
    
    # Helper methods
    def check(self, type: TokenType) -> bool:
        """Check if current token is of given type"""
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    def is_at_end(self) -> bool:
        """Check if we've reached the end of tokens"""
        return self.peek().type == TokenType.EOF
    
    def previous(self) -> Token:
        """Get previous token"""
        return self.tokens[self.current_token_index - 1]
    
    def errors(self):
        return self.errors