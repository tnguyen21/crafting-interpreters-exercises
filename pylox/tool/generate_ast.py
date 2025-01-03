import sys

def define_ast(
    output_dir: str,
    base_name: str,
    types: list[str],
    is_stmt: bool = False
):
    path = output_dir + "/" + base_name + ".py"
    with open(path, "w") as f:
        if is_stmt: f.write("from expr import Expr, Variable\n")
        f.write("from my_token import Token\n\n")
        f.write("class " + base_name.capitalize() + ":\n")
        f.write("    def accept(self, visitor):\n")
        f.write("        method_name = 'visit_' + self.__class__.__name__.lower()\n")
        f.write("        method = getattr(visitor, method_name)\n")
        f.write("        return method(self)\n\n")
        
        for type in types:
            class_name, fields = type.split("=")
            class_name, fields = class_name.strip(), fields.strip()
            define_type(f, base_name.capitalize(), class_name, fields)
            f.write("\n")
        
        define_visitor(f, base_name, types)

def define_visitor(
    f: object,
    base_name: str,
    types: list[str]
):
    f.write("class Visitor:\n")
    for type in types:
        type_name = type.split("=")[0].strip()
        f.write("    def visit_" + type_name.lower() + "(self, " + base_name.lower() + ": " + type_name + "): pass\n")
    f.write("\n")

def define_type(
    f: object,
    base_name: str,
    class_name: str,
    fields: str
):
    f.write("class " + class_name + "(" + base_name + "):\n")
    f.write("    def __init__(self, " + fields + "):\n")
    field_list = fields.split(", ")
    names = [field.split(":")[0] for field in field_list]
    self_names = ["self." + name for name in names]
    f.write("        " + ",".join(self_names) + " = " + ",".join(names) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>")
        sys.exit(1)

    output_dir = sys.argv[1]

    define_ast(output_dir, "expr", [
        "Assign   = name: Token, value: Expr",
        "Binary   = left: Expr, operator: Token, right: Expr",
        "Call     = callee: Expr, paren: Token, arguments: [Expr]",
        "Get      = object: Expr, name: Token",
        "Set      = object: Expr, name: Token, value: Expr",
        "Grouping = expr: Expr",
        "Literal  = value: object",
        "Logical  = left: Expr, operator: Token, right: Expr",
        "Unary    = operator: Token, right: Expr",
        "This     = keyword: Token",
        "Super    = keyword: Token, method: Token",
        "Variable = name: Token"
    ])

    define_ast(output_dir, "stmt", [
        "Block      = statements: [Stmt]",
        "Expression = expr: Expr",
        "Function   = name: Token, params: [Token], body: [Stmt]",
        "Class      = name: Token, superclass: Variable, methods: [Function]",
        "If         = condition: Expr, then_branch: Stmt, else_branch: Stmt",
        "Print      = expr: Expr",
        "Return     = keyword: Token, value: Expr",
        "Var        = name: Token, initializer: Expr",
        "While      = condition: Expr, body: Stmt"
    ], is_stmt=True)