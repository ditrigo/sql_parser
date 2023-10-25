def replace_logical_operators(expression):
    while "И(" in expression or "ИЛИ(" in expression:
        i_and = expression.find("И(")
        i_or = expression.find("ИЛИ(")
        if i_and != -1 and (i_or == -1 or i_and < i_or):
            start = i_and
            end = expression.find(")", start)
            sub_expr = expression[start+1:end+1]
            sub_expr = sub_expr.replace(";", " and ")
            expression = expression[:start] + sub_expr + expression[end+1:]
        else:
            start = i_or
            end = expression.find(")", start)
            sub_expr = expression[start+3:end+1]
            sub_expr = sub_expr.replace(";", " or ")
            expression = expression[:start] + sub_expr + expression[end+1:]
    return expression

# Пример использования
logical_expression = 'a + И(a>b;c<d;x==y) ИЛИ(z>w;x==a)'
modified_expression = replace_logical_operators(logical_expression)
print(modified_expression)
