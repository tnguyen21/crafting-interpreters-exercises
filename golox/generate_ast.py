def define_ast(
    base_name: str,
    types: list[str],
    is_stmt: bool = False
):
    path = base_name + ".go"
    with open(path, "w") as f:
        f.write("package main\n\n")
        
        f.write("type Expr interface {\n")
        f.write("    Accept(ExprVisitor) (interface{}, error)\n}\n\n")
        f.write("type ExprVisitor interface {\n")
        for type in types:
            class_name = type.split("=")[0].strip()
            f.write(f"    Visit{class_name}(expr *{class_name})"+" interface{}\n")
        f.write("}\n\n")

        for type in types:
            class_name, fields = type.split("=")
            class_name, fields = class_name.strip(), fields.strip()
            define_type(f, class_name, fields)
        
def define_type(
    f: object,
    class_name: str,
    fields: str
):
    f.write("type " + class_name + " struct {\n")
    field_list = fields.split(", ")
    names_type_tuples = [field.split(" ") for field in field_list]
    for name, type in names_type_tuples:
        f.write(f"    {name.strip()} {type.strip()}\n")
    f.write("}\n\n")
    f.write(f"func (expr *{class_name}) Accept(visitor ExprVisitor)"+"interface{} {\n")
    f.write(f"    return visitor.Visit{class_name}(expr)\n")
    f.write("}\n\n")


if __name__ == "__main__":
    define_ast("expr", [
        "Binary   = left Expr, operator Token, right Expr",
        "Grouping = expr Expr",
        "Literal  = value object",
        "Unary    = operator Token, right Expr",
    ])
