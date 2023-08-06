import sys

def define_ast(
    output_dir: str,
    base_name: str,
    types: list[str]
):
    path = output_dir + "/" + base_name + ".py"
    with open(path, "w") as f:
        f.write("from my_token import Token\n\n")
        f.write("class " + base_name.capitalize() + ":\n")
        # f.write("    pass\n\n")
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
        f.write("    def visit_" + type_name.lower() + "(self, " + base_name.lower() + ": " + type_name + "):\n")
        f.write("        pass\n")
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
    for field in field_list:
        name = field.split(":")[0]
        f.write("        self." + name + " = " + name + "\n")
    f.write("\n")
    # f.write("    def accept(self, visitor):\n")
    # f.write("        return visitor.visit_" + class_name.lower() + "_" + base_name.lower() + "(self)\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>")
        sys.exit(1)

    output_dir = sys.argv[1]

    define_ast(output_dir, "expr", [
        "Binary   = left: Expr, operator: Token, right: Expr",
        "Grouping = expr: Expr",
        "Literal  = value: object",
        "Unary    = operator: Token, right: Expr"
    ])