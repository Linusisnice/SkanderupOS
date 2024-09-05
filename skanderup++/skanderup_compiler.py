import sys
from skanderup_lexer import Lexer
from skanderup_parser import Parser
from skanderup_codegen import CodeGenerator

def compile_skp_to_asm(input_file, output_file):
    with open(input_file, 'r') as f:
        source_code = f.read()

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    codegen = CodeGenerator(ast)
    assembly_code = codegen.generate_code()

    with open(output_file, 'w') as f:
        f.write(assembly_code)

    print(f"Compiled {input_file} to {output_file}")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "source/program.skp"
    output_file = "output.asm"
    compile_skp_to_asm(input_file, output_file)
