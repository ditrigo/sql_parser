import re


dolg = 10
s_1600_4 = 5


def add_prefix(expression):
    def replace(match):
        if match.group(0) not in {'if', 'else', 'and', 'or', 'datetime.today()'}:
            modified_vars.append(eval(match.group(0)))  # Добавляем переменную в массив
            return 'imported_attr.' + match.group(0)
        else:
            return match.group(0)

    pattern = r'([a-zA-Z_]\w*)'
    modified_vars = []  # Создаем массив для переменных
    modified_expression = re.sub(pattern, replace, expression)
    return modified_vars

def replace_variables(expression, variables):
    def replace(match):
        var_name = match.group(1)
        if var_name in variables:
            return var_name
        else:
            return match.group(0)

    pattern = r'\b([a-zA-Z_]\w*)\b'
    modified_expression = re.sub(pattern, replace, expression)
    return modified_expression
    


expression = "(0 if dolg==0 else (-15 if s_1600_4==0 and dolg>0 else (-15 if dolg/s_1600_4>0.25 else 0)))"

modified_vars = add_prefix(expression)

variable_dict = {var: var for var in modified_vars}

print(variable_dict)

modified_expression = replace_variables(expression, variable_dict)
print(modified_expression)