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

        for i, token in enumerate(tokens):

            if token.isnumeric():
                if i>2 and tokens[i-1] == '-':
                    if tokens[i-2] in (',', '(', '>', '<', '>=', '<=', '==', '!=', '='):
                        items.pop()
                        items.append(('number', "-" + token))
                    else:
                        items.append(('number', token))
                else:
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
    prev_item = None
    prev_prev = None
    
    i = 0

    for item in sublist:

        if item[0] == 'condition':

            if prev_item != 'dot':

                if prev_prev == 'number':
                    mas[i] += f"\n{tabs}ELSE\n\tv_mas[{i}] := v_mas[{i+1}];"
                elif prev_item == 'comparison':
                    mas[i] += "\nIF"
                # elif prev_item == 'delin':
                #     mas[i] += "\nIF "
                else:
                    mas[i] += f" v_mas[{i+1}] "
                
                i += 1
                mas.append(f"\n{tabs}IF")
                print("+++")
                sql_query_end += "\nEND IF;"

            else:
                mas[i] += f"{tabs}IF"
                sql_query_end += "\nEND IF;"

            prev_prev = prev_item
            prev_item = 'condition'
        
        elif item[0] == 'word':   
            mas[i] += f" {item[1]} "
            prev_prev = prev_item
            prev_item = 'word'

        elif item[0] == 'delin':  # +-*/
            mas[i] += f"{item[1]}"
            prev_prev = prev_item
            prev_item = 'delin'

        elif item[0] == 'comparison':  # <>=
            mas[i] += f"{item[1]}"
            prev_prev = prev_item
            prev_item = 'comparison'

        elif item[0] == 'number':   # 123
            if prev_item == 'comparison' or prev_item == 'delin':
                mas[i] += f" {item[1]} "
            elif prev_prev == 'number':
                mas[i] += f"\n{tabs}ELSE\n{tabs}\tv_mas[{i}] := {item[1]};"
            elif prev_prev == 'paren' or prev_prev == 'delin':
                mas[i] += f"{item[1]}"
            else:
                mas[i] += f"\n{tabs}\tv_mas[{i}] := {item[1]};"
            prev_prev = prev_item
            prev_item = 'number'

        elif item[0] == 'paren':   # ()            
            if item[1] == ')':
                sql_query += mas[i]
                print(mas[i])
                print("------------")
                mas[i] = "\nIF "
                i -= 1
            prev_prev = prev_item
            prev_item = 'paren'

        else:
            try:
                element = mas[i+1]
                mas[i] += f"v_mas[{i+1}]"
                print("----------")
            except IndexError:
                if item[0] == 'dot':
                    prev_prev = prev_item
                    prev_item = 'dot'

        if prev_prev == 'comparison':
                mas[i] += "THEN"

    sql_query += sql_query_end

    return sql_query


def sql_query_init():
    sql_query = ""
    inn = 23445667

    sql_query = f'''CREATE FUNCTION if EXISTS f_rate()
RETURNS INTEGER
LANGUAGE PLPGSQL
AS
$$
    DELCARE
        v_rate INTEGER;
        v_mas INTEGER[];
        v_origin varchar(255);
        v_value INTEGER;
    BEGIN
        EXECUTE \"SELECT origin FROM main_catalog_fileds WHERE filed_name LIKE \"|| <filed_name (сальдо)> into v_origin;
        EXECUTE \"SELECT\" || v_origin || \"FROM csv_attributes WHERE inn LIKE\" || <inn ({inn})> into v_value;\n\n'''


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

    user_string = "условие(сальдо+условие(вклад>300, 5, условие(выручка>123, 333, 444))>100, 2, 10) + условие(условие(долг<500, 13, 17)-кредит>200, 7, 9) - условие(штраф<300, 11, 12)"

    sql_query = sql_parser(user_string)
    # print(sql_query)

    with open('generated_query.sql', 'w', encoding='utf-8-sig') as f:
        f.write(sql_query)
