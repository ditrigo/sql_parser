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

    print(tokens)
    print(delimiters)
    return tokens, delimiters


def lexer(contents):
    lines = contents.split('\n')

    nLines = []
    for line in lines:
        chars = list(line)
        temp_str = ""
        tokens = []
        
        # print("expression----------------")
        # print(line)

        tokens.append(temp_str)
        items = []
        
        tokens = re.findall(r'\b\w+\b|[-+*/><=(),]', line)

        # print("tokens----------------")
        # print(tokens)

        for token in tokens:
            if token.isnumeric():
                items.append(('number', token))
            elif token in ('+', '-', '*', '/'):
                items.append(('delin', token))
            elif token in ('>', '<', '>=', '<=', '==', '!='):
                items.append(('comparison', token))
            elif token in ('(', ')'):
                items.append(('paren', token))
            elif token == 'условие':
                items.append(('condition', token))
            elif token != ',':
                items.append(('word', token))

        nLines.append(items)

        # print("nLines----------------")
        # print(nLines, "\n")
    return nLines


def items_to_string(sublist):

    sql_query = ""
    mas = []
    mas.append("")
    tabs = ""

    prev_item = None
    prev_prev = None
    
    i = 0

    for item in sublist:

        if item[0] == 'condition':
            if prev_item != 'dot':
                if prev_prev == 'number':
                    mas[i] += f"\n{tabs}ELSE\n\tmas[{i}] := mas[{i+1}];"
                else:
                    mas[i] += f"mas[{i+1}]"
                i += 1
                # tabs += "\t"
                mas.append(f"\n{tabs}IF ")
            else:
                mas[i] += f"{tabs}IF"
            prev_prev = prev_item
            prev_item = 'condition'
        
        elif item[0] == 'word':     
            mas[i] += f"{item[1]}"
            # else:
            #     temp = "IF"
            prev_prev = prev_item
            prev_item = 'word'

        elif item[0] == 'delin':  # +-*/
            mas[i] += f" {item[1]} "
            prev_prev = prev_item
            prev_item = 'delin'

        elif item[0] == 'comparison':  # <>=
            mas[i] += f" {item[1]} "
            prev_prev = prev_item
            prev_item = 'comparison'

        elif item[0] == 'number':   # 123
            if prev_item == 'comparison':
                mas[i] += f"{item[1]}"
            elif prev_prev == 'number':
                mas[i] += f"\n{tabs}ELSE\n{tabs}\tmas[{i}] := {item[1]};"
            elif prev_prev == 'paren' or prev_prev == 'delin':
                mas[i] += f"{item[1]}"
            else:
                mas[i] += f"\n{tabs}\tmas[{i}] := {item[1]};"
            prev_prev = prev_item
            prev_item = 'number'

        elif item[0] == 'paren':   # ()            
            if item[1] == ')':
                sql_query += mas[i]
                mas[i] = ""
                i -= 1
            prev_prev = prev_item
            prev_item = 'paren'

        else:
            try:
                element = mas[i+1]
                mas[i] += f"mas[{i+1}]"
                print("----------")
            except IndexError:
                if item[0] == 'dot':
                    prev_prev = prev_item
                    prev_item = 'dot'

        if prev_prev == 'comparison':
                mas[i] += " THEN"


    return sql_query


def sql_parser(content):

    expressions, delimiters = split_expression(content)
    sql_result = ""

    print("\n\n")
    # print("expressions----------------")
    # print(expressions, "\n")

    express_list = []
    for expression in expressions:
        express = lexer(expression)
        express_list.append(express)

    for expr in express_list:
        for ex in expr:
            # print(ex)
            lst = items_to_string(ex)
            print(lst)
            sql_result += lst

    
    return sql_result


if __name__ == '__main__':

    user_string = "условие(сальдо+условие(вклад>300, 5, условие(выручка>123, 333, 444))>100, 2, 10) + условие(условие(долг<500, 13, 17)-кредит>200, 7, 9) - условие(штраф<300, 11, 12)"

    sql_query = sql_parser(user_string)
    # print(sql_query)
