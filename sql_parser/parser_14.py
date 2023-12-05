import regex as re

def split_expression(s):

    tokens = []
    delimiters = []
    current_condition = ""
    open_brackets = 0

    operators = set('+-*/')

    for char in s:
        if char == '(':
            open_brackets += 1
        elif char == ')':
            open_brackets -= 1

        if open_brackets == 0 and char in operators:
            if current_condition:
                tokens.append(current_condition.strip())
            delimiters.append(char)
            current_condition = ""
        else:
            current_condition += char

    if current_condition:
        tokens.append(current_condition.strip())

    # print(tokens)
    # print(delimiters)
    return tokens, delimiters


def lexer(contents):

    lines = contents.split('\n')

    nLines = []

    for line in lines:

        temp_str = ""
        tokens = []
        
        tokens.append(temp_str)
        items = []
        
        tokens = re.findall(r'\b\w+\b|[-+*/><=(),]', line)

        for token in tokens:
            if token.isnumeric():
                items.append(('number', token))
            elif token in ('+', '-', '*', '/'):
                items.append(('delin', token))
            elif token in ('>', '<', '>=', '<=', '==', '!=', '='):
                items.append(('comparison', token))
            elif token in ('(', ')'):
                items.append(('paren', token))
            elif token == 'условие':
                items.append(('condition', token))
            elif token != ',':
                items.append(('word', token))

        nLines.append(items)
    print(nLines)
    return nLines


def items_to_string(sublist):

    sql_query = ""
    mas = []
    mas.append("")
    tabs = ""
    sql_query_end = ""

    print(sublist[-2], "--------")
    print(len(sublist))
    i = 0

    for index in range(0, len(sublist)):

        if sublist[index][0] == 'condition':
            if sublist[index-1][0] != 'dot' and index-1 >= 0:
                if sublist[index-2] == 'number' and index-2 >= 0:
                    mas[i] += f"\n{tabs}ELSE\n\tv_mas[{i}] := v_mas[{i+1}];"
                elif sublist[index-1] == 'comparison' and index-1 >= 0:
                    mas[i] += "\nIF "
                elif index-1 >= 0 and index-2 >= 0:
                    mas[i] += f"v_mas[{i+1}]"
                i += 1
                mas.append(f"\n{tabs}IF ")
                sql_query_end += "\nEND IF;"
            elif index-1 >= 0 and index-2 >= 0:
                mas[i] += f"{tabs}IF"
                sql_query_end += "\nEND IF;"
        
        elif sublist[index][0] == 'word':   
            mas[i] += f"{sublist[index][1]}"

        elif sublist[index][0] == 'delin':  # +-*/
            mas[i] += f" {sublist[index][1]} "

        elif sublist[index][0] == 'comparison':  # <>=
            mas[i] += f" {sublist[index][1]} "

        elif sublist[index][0] == 'number':   # 123
            if sublist[index-1] == 'comparison' and index-1 >= 0:
                mas[i] += f"{sublist[index][1]}"
            elif sublist[index-2] == 'number' and index-2 >= 0:
                mas[i] += f"\n{tabs}ELSE\n{tabs}\tv_mas[{i}] := {sublist[index][1]};"
            elif (sublist[index-2] == 'paren' or sublist[index-2] == 'delin') and index-2 >= 0:
                mas[i] += f"{sublist[index][1]}"
            elif index-1 >= 0 and index-2 >= 0:
                mas[i] += f"\n{tabs}\tv_mas[{i}] := {sublist[index][1]};"

        elif sublist[index][0] == 'paren':   # ()            
            if sublist[index][1] == ')':
                sql_query += mas[i]
                mas[i] = ""
                i -= 1

        else:
            try:
                element = mas[i+1]
                mas[i] += f"v_mas[{i+1}]"
                print("----------")
            except IndexError:
                pass

        if sublist[index-2] == 'comparison' and index-2 >= 0:
                mas[i] += " THEN"

    sql_query += sql_query_end

    return sql_query


def sql_query_init():
    sql_query = ""
    inn = 23445667

    sql_query = "CREATE FUNCTION if EXISTS f_rate()\nRETURNS INTEGER\nLANGUAGE PLPGSQL\nAS\n$$\n"  # noqa: E501
    sql_query += "\tDECLARE\n\t\tv_rate INTEGER;\n\t\tv_mas INTEGER[];\n\t\tv_origin varchar(255);\n\t\tv_value INTEGER;\n\tBEGIN\n\n"
    sql_query += "\t\tEXECUTE \"SELECT origin FROM main_catalog_fileds WHERE filed_name LIKE \"|| <filed_name (сальдо)> into v_origin;\n"
    sql_query += f"\t\tEXECUTE \"SELECT\" || v_origin || \"FROM csv_attributes WHERE inn LIKE\" || <inn ({inn})> into v_value;\n\n"

    return sql_query


def sql_parser(content):

    expressions, delimiters = split_expression(content)
    sql_result = sql_query_init()
    index = 0

    express_list = []
    for expression in expressions:
        express = lexer(expression)
        express_list.append(express)

    for expression in express_list:
        for ex in expression:

            lst = items_to_string(ex)

            sql_result += lst

            if index == 0:
                sql_result += f"\n\nv_result = v_mas[1];\n"
                index += 1
            else:
                sql_result += f"\n\nv_result = v_result {delimiters[index-1]} v_mas[1];\n"
                index += 1
            
    sql_result += "\n\t\treturn v_result;\n\tEND;\n$$"
    
    return sql_result


if __name__ == '__main__':

    user_string = "условие(сальдо+условие(вклад>300, 5, условие(выручка>123, 333, 444))>100, 2, 10) + условие(условие(долг<500, 13, 17)-кредит>200, 7, 9) - условие(штраф<300, 11, условие(что_то=999, 45, 56))"

    sql_query = sql_parser(user_string)
    print(sql_query)

    with open('generated_query.sql', 'w', encoding='utf-8-sig') as f:
        f.write(sql_query)
