class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        ast = []
        while self.current < len(self.tokens):
            token_type, token_value = self.tokens[self.current]
            if token_type == 'ID':
                ast.append(self.parse_statement())
            elif token_type == 'FUNCTION':
                ast.append(self.parse_function())
            elif token_type == 'INT':
                ast.append(self.parse_declaration())
            else:
                self.current += 1  # Skip over any unrecognized tokens (e.g., newlines)
        return ast

    def parse_statement(self):
        # Skip over newlines
        while self.current < len(self.tokens) and self.tokens[self.current][0] == 'NEWLINE':
            self.current += 1

        if self.current >= len(self.tokens):
            return None  # End of input

        identifier = self.tokens[self.current][1]
        self.current += 1

        if identifier == 'print':
            expr = self.parse_expression()
            return ('print', expr)

        if self.current < len(self.tokens) and self.tokens[self.current][0] == 'ASSIGN':
            self.current += 1
            expr = self.parse_expression()
            return ('assign', identifier, expr)

        elif identifier in {'if', 'while'}:
            condition = self.parse_expression()
            body = self.parse_block()
            return (identifier, condition, body)

        else:
            raise SyntaxError(f"Unexpected statement: {identifier}")

    def parse_declaration(self):
        # Expecting 'int' keyword, followed by a variable name
        self.current += 1  # Skip 'int'
        var_name = self.tokens[self.current][1]
        self.current += 1  # Skip variable name

        if self.tokens[self.current][0] == 'ASSIGN':
            self.current += 1  # Skip '='
            expr = self.parse_expression()
            return ('declare', 'int', var_name, expr)

        return ('declare', 'int', var_name, None)

    def parse_expression(self):
        term = self.parse_term()
        while self.current < len(self.tokens) and self.tokens[self.current][0] in {'OP', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE', 'LPAREN'}:
            if self.tokens[self.current][0] in {'OP', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE'}:
                op = self.tokens[self.current][1]
                self.current += 1
                term = ('binop', op, term, self.parse_term())
            elif self.tokens[self.current][0] == 'LPAREN':
                # Parse a function call or grouped expression
                self.current += 1  # Skip '('
                args = []
                while self.tokens[self.current][0] != 'RPAREN':
                    args.append(self.parse_expression())
                    if self.tokens[self.current][0] == 'COMMA':
                        self.current += 1  # Skip ',' between arguments
                self.current += 1  # Skip ')'
                term = ('call', term, args)
        return term

    def parse_term(self):
        token_type, token_value = self.tokens[self.current]
        if token_type == 'NUMBER':
            self.current += 1
            return ('num', token_value)
        elif token_type == 'STRING':
            self.current += 1
            return ('string', token_value)
        elif token_type == 'ID':
            self.current += 1
            return ('var', token_value)
        elif token_type == 'LPAREN':
            # Handle grouped expressions
            self.current += 1  # Skip '('
            expr = self.parse_expression()
            if self.tokens[self.current][0] != 'RPAREN':
                raise SyntaxError(f"Expected ')', found {self.tokens[self.current][1]}")
            self.current += 1  # Skip ')'
            return expr
        else:
            raise SyntaxError(f"Unexpected term: {token_value}")

    def parse_function(self):
        self.current += 1  # Skip 'function'
        func_name = self.tokens[self.current][1]
        self.current += 1  # Skip the function name

        args = []
        self.current += 1  # Skip the opening parenthesis
        while self.tokens[self.current][0] != 'RPAREN':
            if self.tokens[self.current][0] == 'ID':
                args.append(self.tokens[self.current][1])
            self.current += 1
        self.current += 1  # Skip closing parenthesis

        body = self.parse_block()
        return ('function', func_name, args, body)

    def parse_block(self):
        self.current += 1  # Skip '{'
        body = []
        while self.tokens[self.current][0] != 'RBRACE':
            statement = self.parse_statement()
            if statement is not None:
                body.append(statement)
        self.current += 1  # Skip '}'
        return body
