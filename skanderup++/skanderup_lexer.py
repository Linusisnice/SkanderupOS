import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current = 0

    def tokenize(self):
        token_specification = [
            ('NUMBER', r'\d+'),
            ('ASSIGN', r'='),
            ('END', r';'),
            ('COMMA', r','),            # Match commas
            ('INT', r'int'),            # Match 'int' keyword
            ('ID', r'[A-Za-z_]\w*'),
            ('STRING', r'"[^"]*"'),     # Match double-quoted strings
            ('LPAREN', r'\('),          # Left parenthesis
            ('RPAREN', r'\)'),          # Right parenthesis
            ('LBRACE', r'\{'),          # Left brace
            ('RBRACE', r'\}'),          # Right brace
            ('OP', r'[+\-*/]'),         # Arithmetic operators
            ('GT', r'>'),               # Greater than
            ('LT', r'<'),               # Less than
            ('GE', r'>='),              # Greater than or equal
            ('LE', r'<='),              # Less than or equal
            ('EQ', r'=='),              # Equal to
            ('NE', r'!='),              # Not equal to
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
            ('COMMENT', r'æ.*'),        # Ignore comments starting with æ
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        for mo in re.finditer(tok_regex, self.source_code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                value = int(value)
            elif kind == 'ID' and value in {'if', 'else', 'while', 'function', 'return'}:
                kind = value.upper()
            elif kind == 'STRING':
                value = value[1:-1]  # Remove quotes from the string value
            elif kind == 'NEWLINE':
                self.tokens.append(('NEWLINE', '\\n'))
                continue
            elif kind == 'SKIP' or kind == 'COMMENT':
                continue  # Skip over comments and spaces/tabs
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {self.current}')
            self.tokens.append((kind, value))
        return self.tokens
