from sys import argv
import regex as re


def split_expression(input_string):

    operators = r'\s*[-+*/]\s*'

    matches = re.split(operators, input_string)

    delimiters = re.findall(operators, input_string)
    delimiters = [d.replace(' ', '') for d in delimiters]

    return matches, delimiters


def lexer(contents):
    lines = contents.split('\n')

    nLines = []
    for line in lines:
        chars = list(line)
        temp_str = ""
        tokens = []

        for char in chars:
            if char == ",":
                tokens.append(temp_str)
                temp_str = ""
            else:
                temp_str += char

        tokens.append(temp_str)
        items = []

        pattern = r"\s*условие\s*\("

        for token in tokens:    
            
            if re.match(pattern, token):
                token = re.sub(r"условие\s*\(", "", token)
                token = token.replace(" и ", " AND ")
                token = token.replace(" или ", " OR ")
                items.append(("word", token))

            else:
                token = re.sub(r"[^-0-9]", "", token)
                items.append(("number", token))

        nLines.append(items)

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
    j = 0

    
    for index, expr in enumerate(data):

        prev_type = None

        for sublist in expr:
            
            for item in sublist:

                if item[0] == 'word':
            
                    if prev_type == 'number':
                        sql_query += f"{tabs[:-1]}ELSE\n"
                    sql_query += f"{tabs}IF {item[1]} THEN\n"
                    prev_type = 'word'
                    end += f"{tabs}END IF;\n"
                    tabs += "\t"
                

                elif item[0] == 'number':
                    if prev_type == 'number':
                        sql_query += f"{tabs[:-1]}ELSE\n"
                    sql_query += f"{tabs}{target}[{index}] := {item[1]};\n"
                    prev_type = 'number'
        
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

    content = "условие(сальдо>100, 2, условие(вклад>300, 5, 6)) + условие(кредит>200, 7, 9) - условие(штраф<300, 11, 12)"

    expressions, delimiters = split_expression(content)
    # print(expressions)
    # print("----------------")
    express_list = []
    for expression in expressions:
        express = lexer(expression)
        # print(express)
        # print("----------------")
        express_list.append(express)
        
    # print(express_list)
    # print("----------------")
    lst = generate_sql_query(express_list, delimiters)
    print(lst)
    # print("----------------")
    # print(delimiters)

    with open('generated_query.sql', 'w', encoding='utf-8-sig') as f:
        f.write(lst)
