from sys import argv
import regex as re


def split_expression(input_string):

    operators = r'\)\s*[-+*/]\s*'
    operators_delim = r'\s*[-+*/]\s*'

    matches = re.split(operators, input_string)

    delimiters = re.findall(operators_delim, input_string)
    delimiters = [d.replace(' ', '') for d in delimiters]

    return matches, delimiters


def extract_condition(token):
    pattern = r'[^-+*/]?\s*условие\([^)]*\)\s*[<>]=?'
    match = re.search(pattern, token)
    if match:
        return match.group(0)
    return None


def lexer(contents):
    lines = contents.split('\n')

    nLines = []
    for line in lines:
        chars = list(line)
        temp_str = ""
        tokens = []
        
        print("expression----------------")
        print(line)
        # for char in chars:
        #     if char == ",":
        #         tokens.append(temp_str)
        #         temp_str = ""
        #     else:
        #         temp_str += char

        tokens.append(temp_str)
        items = []
        
        tokens = re.findall(r'\b\w+\b|[-+*/><=(),]', line)
        

        pattern_word = r"\s*условие\s*\("
        pattern_numb = r"[^-0-9]"
        # pattern_if = r"[^-+=<>]"
        pattern_in = r"условие\((.*?)\)(?=[+\-*/])"

        prev_type = None

        print("tokens----------------")
        print(tokens)

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

        print("nLines----------------")
        print(nLines, "\n")
    return nLines


def generate_sql_query(data, delimiters):

    inn = 23445667

    sql_query = "CREATE FUNCTION if EXISTS f_rate()\nRETURNS INTEGER\nLANGUAGE PLPGSQL\nAS\n$$\n"  # noqa: E501
    sql_query += "\tDECLARE\n\t\tv_rate INTEGER;\n\t\tv_mas INTEGER[];\n\t\tv_origin varchar(255);\n\t\tv_value INTEGER;\n\tBEGIN\n\n"
    sql_query += "\t\tEXECUTE \"SELECT origin FROM main_catalog_fileds WHERE filed_name LIKE \"|| <filed_name (сальдо)> into v_origin;\n"
    sql_query += f"\t\tEXECUTE \"SELECT\" || v_origin || \"FROM csv_attributes WHERE inn LIKE\" || <inn ({inn})> into v_value;\n\n"
    
    target = "v_mas"
    end = ""
    end_expr = "\n\t\tv_rate = "
    tabs = "\t\t"

    sql_query_end = ""
    sql_query_temp = ""
    mas = []
    mas.append("")
    i = 0
    comp_temp = ""

    
    for index, expr in enumerate(data):

        prev_item = None
        prev_prev = None

        for sublist in expr:
            
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

                
        
            if sublist != expr[-1]:
                sql_query += f"{tabs}ELSE\n"
        
        tabs = "\t\t"
        sql_query += "\n"
    
    for index, delimiter in enumerate(delimiters):
        end_expr = end_expr + f"{target}[{index}] {delimiter} "

    end_expr += f"{target}[{len(delimiters)}];\n\t\treturn v_rate;\n"

    sql_query += f"{tabs}{end}{end_expr}\n\tEND;\n$$;"
    
    return sql_query


def parser(str):
    
    lst = lexer(str)
    sql_query = generate_sql_query(lst)

    return sql_query


if __name__ == '__main__':

    content = "условие(сальдо+условие(вклад>300, 5, условие(выручка>123, 333, 444))>100, 2, 10)"

    expressions, delimiters = split_expression(content)

    print("\n\n")
    print("expressions----------------")
    print(expressions, "\n")
    
    express_list = []
    for expression in expressions:
        express = lexer(expression)
        
        # print("express----------------")
        # print(express)
        
        express_list.append(express)
        
    # print("express_list----------------")
    # print(express_list)

    lst = generate_sql_query(express_list, delimiters)
    
    # print(lst)
    # print("----------------")
    # print(delimiters)
    # print("----------------")
    print("\n\n")
    with open('generated_query.sql', 'w', encoding='utf-8-sig') as f:
        f.write(lst)
