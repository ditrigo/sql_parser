# pyparser_6_2.py copy

def pyparser(str):
    if not str:
        return []
    res = []
    i = 0
    cond_counter = 0
    res_counter = 0
    while i<len(str):

        if str[i] == "у" and str[i:i+8] == "условие(":

            if cond_counter == 0: 
                cond_start = i+8

                if str[0:i] != '':
                    res.append("add_before")
                    res.append(str[0:i])
            
            cond_counter += 1
            i += 7

        elif str[i] == ")":

            if cond_counter == 1:
                res2_end = i
                result_1 = pyparser(str[res2_start:res2_end])

                res.append("res2")
                res.append(result_1)

                
                if str[i+1:] != '':
                    res.append("add_after")
                    res.append(str[i+1:])

            cond_counter -= 1

        elif str[i] == ";" and cond_counter == 1:
            if res_counter == 0:
                res_counter += 1
                cond_end = i
                res1_start = i+1
                result_1 = pyparser(str[cond_start:cond_end])

                res.append("cond")
                res.append(result_1)
                
            elif res_counter == 1:
                res_counter = 0
                res1_end = i
                res2_start = i+1
                result_1 = pyparser(str[res1_start:res1_end])

                res.append("res1")
                res.append(result_1)
            
        i += 1

    if res == []:
        return str
    else:
        return res


def generate_condition_string(lst):
    result = ""
    i = 0
    while i < len(lst):
        
        if lst[i] == "cond":
            cond = generate_condition_string(lst[i+1])
            res1 = generate_condition_string(lst[i+3])
            res2 = generate_condition_string(lst[i+5])
            result += f"({res1} if {cond} else {res2})"
 
            i += 6

        elif isinstance(lst[i], list):
            result += generate_condition_string(lst[i])
            i += 1

        else:
            if lst[i] == "add_before" or lst[i] == "add_after":
                result += str(lst[i+1])
                i += 2

            else:
                result += str(lst[i])
                i += 1

    return result


def replace_operators(expression):

    expression = expression.replace("=", "==")
    expression = expression.replace("<>", "!=")
    expression = expression.replace(",", ".")

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


expression = 'условие(dolg=0;0;условие(s_1600_4=0 and dolg>0;-15;условие(dolg/s_1600_4>0,25;-15;0)))'

result = pyparser(expression)
result_1 = generate_condition_string(result)
result_2 = replace_operators(result_1)


# Correct answer: 
# 0 if (dolg == 0) else (-15 if (s_1600_4 == 0 and dolg > 0) else (-15 if dolg / s_1600_4 > 0.25 else 0))")

print(result_2)

# Выполнение в питоне
try:
    dolg = 5
    s_1600_4 = 1
    answer = eval(result_2)
    print("Answer:", answer)
except SyntaxError:
    print("ну гг")
