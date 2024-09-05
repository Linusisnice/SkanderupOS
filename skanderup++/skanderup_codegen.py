class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.assembly_code = ""

    def generate_code(self):
        for node in self.ast:
            if node[0] == 'assign':
                self.assembly_code += self.generate_assign(node)
            elif node[0] == 'function':
                self.assembly_code += self.generate_function(node)
            elif node[0] == 'print':
                self.assembly_code += self.generate_print(node)
            elif node[0] in {'if', 'while'}:
                self.assembly_code += self.generate_condition(node)
            else:
                raise ValueError(f"Unknown AST node: {node[0]}")
        return self.assembly_code

    def generate_assign(self, node):
        identifier, expr = node[1], node[2]
        code = ""
        if expr[0] == 'num':
            code += f"mov [{identifier}], {expr[1]}\n"
        elif expr[0] == 'var':
            code += f"mov eax, [{expr[1]}]\nmov [{identifier}], eax\n"
        elif expr[0] == 'binop':
            code += self.generate_binop(expr)
            code += f"mov [{identifier}], eax\n"
        return code

    def generate_function(self, node):
        func_name, args, body = node[1], node[2], node[3]
        code = f"{func_name}:\n"
        for stmt in body:
            if stmt[0] == 'assign':
                code += self.generate_assign(stmt)
            elif stmt[0] == 'print':
                code += self.generate_print(stmt)
        code += "ret\n"
        return code

    def generate_print(self, node):
        expr = node[1]
        code = ""
        if expr[0] == 'string':
            for char in expr[1]:
                code += f"mov al, '{char}'\n"
                code += "mov ah, 0x0E\n"
                code += "int 0x10\n"
        return code

    def generate_binop(self, node):
        op, left, right = node[1], node[2], node[3]
        code = ""
        if left[0] == 'num':
            code += f"mov eax, {left[1]}\n"
        elif left[0] == 'var':
            code += f"mov eax, [{left[1]}]\n"
        if right[0] == 'num':
            code += f"{self.op_to_asm(op)} eax, {right[1]}\n"
        elif right[0] == 'var':
            code += f"{self.op_to_asm(op)} eax, [{right[1]}]\n"
        return code

    def op_to_asm(self, op):
        if op == '+':
            return "add"
        elif op == '-':
            return "sub"
        elif op == '*':
            return "imul"
        elif op == '/':
            return "idiv"
        elif op in {'>', '<', '>=', '<=', '==', '!='}:
            return self.generate_comparison(op)
        else:
            raise ValueError(f"Unknown operator: {op}")

    def generate_comparison(self, op):
        # Handle comparisons (assuming basic comparisons for simplicity)
        comparison_map = {
            '>': 'jg',   # Jump if greater
            '<': 'jl',   # Jump if less
            '>=': 'jge', # Jump if greater or equal
            '<=': 'jle', # Jump if less or equal
            '==': 'je',  # Jump if equal
            '!=': 'jne'  # Jump if not equal
        }
        return comparison_map[op]

    def generate_condition(self, node):
        keyword, condition, body = node[0], node[1], node[2]
        code = ""
        if condition[0] == 'binop':
            code += self.generate_binop(condition)
        code += f"{keyword}:\n"
        for stmt in body:
            code += self.generate_assign(stmt)
        return code
