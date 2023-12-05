import ast

def parse_line(line):
    """ Parse a single line of the format 'condition(a, b, c)' or 'condition(a, b, c, d)' """
    parts = line.split(' ')
    cond, op, left, right = parts[:4]
    if len(parts) > 4:
        raise ValueError("Invalid syntax")
    
    # Handle nested conditions
    nesting = 0
    while parts[nesting+4] == 'condition':
        nested_cond, nested_op, nested_left, nested_right = parts[nesting+4:]
        if nested_op != ',' and nested_op != ':':
            raise ValueError("Invalid syntax")
        left = parse_line(nested_left)
        right = parse_line(nested_right)
        parts = [cond, op, left, right] + parts[nesting+4:]
        nesting += 1
    
    return ast.parse(parts[0], parts[1], parts[2], parts[3])

def eval_ast(node):
    """ Evaluate an abstract syntax tree (AST) node """
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Str):
        return str(node.s)
    elif isinstance(node, ast.List):
        return [eval_ast(child) for child in node.elts]
    elif isinstance(node, ast.Tuple):
        return tuple([eval_ast(child) for child in node.elts])
    elif isinstance(node, ast.IfExp):
        cond = eval_ast(node.test)
        if cond:
            return eval_ast(node.body)
        else:
            return eval_ast(node.orelse)
    elif isinstance(node, ast.Call):
        func = eval_ast(node.func)
        args = [eval_ast(arg) for arg in node.args]
        return func(*args)
    else:
        raise ValueError("Unsupported AST node type")

# Test the parser
lines = ["condition(balance>100, 2, condition(contribution>300, 5, 6))",
         "condition(credit>200, 7, 9)",
         "condition(age>18, 'adult', 'minor')"]
for line in lines:
    print(parse_line(line))

# Use the parser to generate code
asp_code = "\n".join(["condition(balance>100, 2, condition(contribution>300, 5, 6))",
                      "condition(credit>200, 7, 9)",
                      "condition(age>18, 'adult', 'minor')"])
print(ast.parse(asp_code).body)

# Evaluate the generated code
v_temp = [0, 0]
v_rate = 0
for node in ast.parse(asp_code).body:
    if isinstance(node, ast.Assign):
        v_temp[int(node.target)] = eval_ast(node.value)
    elif isinstance(node, ast.Add):
        v_rate += eval_ast(node.op1) + eval_ast(node.op2)
    else:
        raise ValueError("Unsupported AST node type")
print(f"v_temp = {v_temp}")
print(f"v_rate = {v_rate}")