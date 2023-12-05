from datetime import datetime
import re
from sympy import sympify


def parser_expression(expression):

    if not expression:
        return []
    
    res = []
    i = 0
    cond_counter = 0
    res_counter = 0
    blanket_counter = 0

    while i<len(expression):

        if expression[i] == "у" and expression[i:i+8] == "условие(":

            if cond_counter == 0: 
                cond_start = i+8

                if expression[0:i] != '':
                    res.append("add_before")
                    res.append(expression[0:i])
            
            cond_counter += 1
            i += 7

        elif expression[i] == "(":

            blanket_counter += 1

        elif expression[i] == ")":

            if blanket_counter == 0:

                if cond_counter == 1:
                    res2_end = i
                    result_1 = parser_expression(expression[res2_start:res2_end])

                    res.append("res2")
                    res.append(result_1)

                    if expression[i+1:] != '':
                        res.append("add_after")
                        res.append(expression[i+1:])

                cond_counter -= 1

            else:
                blanket_counter -= 1

            

        elif expression[i] == ";" and cond_counter == 1:

            if res_counter == 0:
                res_counter += 1
                cond_end = i
                res1_start = i+1
                result_1 = parser_expression(expression[cond_start:cond_end])

                res.append("cond")
                res.append(result_1)
                
            elif res_counter == 1:
                res_counter = 0
                res1_end = i
                res2_start = i+1
                result_1 = parser_expression(expression[res1_start:res1_end])

                res.append("res1")
                res.append(result_1)
            
        i += 1

    if res == []:
        return expression
    else:
        return res


def generate_condition_string(expression):

    result = ""
    i = 0

    while i < len(expression):
        
        if expression[i] == "cond":
            cond = generate_condition_string(expression[i+1])
            res1 = generate_condition_string(expression[i+3])
            res2 = generate_condition_string(expression[i+5])
            result += f"({res1} if {cond} else {res2})"
 
            i += 6

        elif isinstance(expression[i], list):
            result += generate_condition_string(expression[i])
            i += 1

        else:
            if expression[i] == "add_before" or expression[i] == "add_after":
                result += str(expression[i+1])
                i += 2

            else:
                result += str(expression[i])
                i += 1

    return result


def pre_replace(expression):

    expression = re.sub(r'(?<![<=>!])=(?!=)', '==', expression)
    expression = expression.replace("<>", "!=")
    expression = expression.replace(",", ".")
    expression = expression.lower().replace(" and ", " and ")
    expression = expression.lower().replace(" or ", " or ")
    expression = expression.replace("||", " or ")
    expression = expression.lower().replace("abs(", "abs(")

    while "и(" in expression.lower() or "или(" in expression.lower():
        i_and = expression.lower().find("и(")
        i_or = expression.lower().find("или(")

        if i_and != -1 and (i_or == -1 or i_and < i_or):
            start = i_and
            end = start + 2
            open_count = 1

            for i in range(start + 2, len(expression)):
                if expression[i] == "(":
                    open_count += 1
                elif expression[i] == ")":
                    open_count -= 1
                    if open_count == 0:
                        end = i
                        break

            sub_expr = expression[start+2:end]
            sub_expr = sub_expr.replace(";", " and ")
            expression = expression[:start] + sub_expr + expression[end+1:]

        else:
            start = i_or
            end = start + 4
            open_count = 1

            for i in range(start + 4, len(expression)):
                if expression[i] == "(":
                    open_count += 1
                elif expression[i] == ")":
                    open_count -= 1
                    if open_count == 0:
                        end = i
                        break

            sub_expr = expression[start+4:end]
            sub_expr = sub_expr.replace(";", " or ")
            expression = expression[:start] + sub_expr + expression[end+1:]

    while "непоиск(" in expression.lower():
        start = expression.lower().find("непоиск(")
        end = expression.find(")", start)
        sub_expr = expression[start+8:end]
        search_term, search_in = sub_expr.split(";")
        replacement = f'{search_term} not in {search_in}'
        expression = expression[:start] + replacement + expression[end+1:]

    while "поиск(" in expression.lower():
        start = expression.lower().find("поиск(")
        end = expression.find(")", start)
        sub_expr = expression[start+6:end]
        search_term, search_in = sub_expr.split(";")
        replacement = f'{search_term} in {search_in}'
        expression = expression[:start] + replacement + expression[end+1:]

    while "разндат(" in expression.lower():
        start = expression.lower().find("разндат(")
        end = expression.find('")', start)
        sub_expr = expression[start+8:end+1]
        args = sub_expr.split(";")
        if args[1].lower() == "сегодня()":
            args[1] = "datetime.today()"
        unit = args[2]  

        if unit == '"y"':
            replacement = f'abs({args[0]} - {args[1]}).days//365'
        elif unit == '"d"':
            replacement = f'abs({args[0]} - {args[1]}).days'
        else:
            replacement = f'abs({args[0]} - {args[1]})'
            
        expression = expression[:start] + replacement + expression[end+2:]

    while "еслиошибка(" in expression.lower():
        error_condition_start = expression.lower().find("еслиошибка(")
        error_condition_end = error_condition_start + len("еслиошибка(")
        count = 1

        for i in range(error_condition_end, len(expression)):
            if expression[i] == "(":
                count += 1
            elif expression[i] == ")":
                count -= 1

            if count == 0:
                error_condition_end = i
                break

        error_condition_expression = expression[error_condition_start + 11:error_condition_end]
        condition_check, expression_if_error = error_condition_expression.split(";")

        denominators = [term.as_numer_denom()[1] for term in sympify(condition_check).as_ordered_terms()]
        conditions_list = [f'{denominator}!=0' for denominator in denominators]
        conditions_result = " and ".join(conditions_list)

        replacement_expression = f'({condition_check} if {conditions_result} else {expression_if_error})'
        expression = expression[:error_condition_start] + replacement_expression + expression[error_condition_end + 1:]


    while "епусто(" in expression.lower():
        empty_check_start = expression.lower().find("епусто(")
        empty_check_end = expression.find(")", empty_check_start)
        sub_expression = expression[empty_check_start + 7:empty_check_end]

        replacement_expression = f'(True if {sub_expression} == "" or {sub_expression} is None else False)'
        expression = expression[:empty_check_start] + replacement_expression + expression[empty_check_end + 1:]

    return expression


def add_prefix(expression):
    def replace(match):
        if match.group(0) not in {'if', 'else', 'and', 'or', 'not', 'in', 'abs', 'datetime', 'today', 'days'}:
            return 'imported_attr.' + match.group(0)
        else:
            return match.group(0)

    pattern = r'([a-zA-Z_]\w*)'
    modified_expression = re.sub(pattern, replace, expression)
    return modified_expression


def var_dict(expression):
    reserved_keywords = {'if', 'else', 'and', 'or', 'datetime.today()', 'not', 'in', 'abs', 'datetime', 'today', 'days'}
    pattern = r'([a-zA-Z_]\w*)'
    modified_vars = {}

    def replace(match):
        nonlocal modified_vars
        var_name = match.group(0)
        if var_name not in reserved_keywords:
            var_value = eval(var_name)
            modified_vars[var_name] = var_value
        return var_name

    modified_expression = re.sub(pattern, replace, expression)
    return modified_vars


def replace_variables(expression, imported_attr):
    vars = var_dict(expression)
    def replace(match):
        var_name = match.group(0)
        if var_name in vars:
            return str(vars[var_name])
        else:
            return var_name

    pattern = r'([a-zA-Z_]\w*)'
    modified_expression = re.sub(pattern, replace, expression)
    return modified_expression


def pyparser(expression):
    try:
        expression = pre_replace(expression)
    except Exception as e:
        return f"Error in pre_replace: {e}"

    try:
        expression = parser_expression(expression)
    except Exception as e:
        return f"Error in parser_expression: {e}"

    try:
        expression = generate_condition_string(expression)
    except Exception as e:
        return f"Error in generate_condition_string: {e}"

    # try:
    #     expression = add_prefix(expression)
    # except Exception as e:
    #     return f"Error in add_prefix: {e}"

    return expression

