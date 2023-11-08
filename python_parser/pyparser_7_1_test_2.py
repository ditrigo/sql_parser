import re

dolg = 10
s_1600_4 = 5

def var_dict(expression):
    reserved_keywords = {'if', 'else', 'and', 'or', 'datetime.today()'}
    pattern = r'([a-zA-Z_]\w*)'
    modified_vars = {}  # Создаем словарь для переменных

    def replace(match):
        nonlocal modified_vars
        var_name = match.group(0)
        if var_name not in reserved_keywords:
            var_value = eval(var_name)
            modified_vars[var_name] = var_value  # Добавляем переменную в словарь
            return var_name
        else:
            return var_name

    modified_expression = re.sub(pattern, replace, expression)
    return modified_vars


def replace_variables(expression, vars):
    def replace(match):
        var_name = match.group(0)
        if var_name in vars:
            return str(vars[var_name])
        else:
            return var_name

    pattern = r'([a-zA-Z_]\w*)'
    modified_expression = re.sub(pattern, replace, expression)
    return modified_expression


expression = "(0 if dolg==0 else (-15 if s_1600_4==0 and dolg>0 else (-15 if dolg/s_1600_4>0.25 else 0)))"
vars = var_dict(expression)
print(vars)
print(replace_variables(expression, vars))
