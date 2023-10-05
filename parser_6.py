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

    comp_temp = ""

    
    for index, expr in enumerate(data):

        prev_type = None

        for sublist in expr:
            
            for item in sublist:
                
                if prev_type == 'comparison':
                    sql_query_end += f"{item[1]}"  


                if item[1] == 'условие':
                    sql_query_end += f"{tabs}IF " 
                
                elif item[0] == 'delin':
                    sql_query_end += f" {item[1]} "

                elif item[1] == '(':
                    sql_query_end = ""
                elif item[1] == ')':
                    sql_query += sql_query_end

                elif item[0] == 'comparison':
                    prev_type = 'comparison'
                    comp_temp = f"{item[1]}"

                elif item[0] == 'word':
            
                    if prev_type == 'number':
                        sql_query_end += f"{tabs[:-1]}ELSE\n"
                    sql_query_end += f"{item[1]}"
                    prev_type = 'word'
                    end += f"{tabs}END IF;\n"
                    tabs += "\t"

                elif item[0] == 'number':
                    if prev_type == 'number':
                        sql_query_end += f"{tabs[:-1]}ELSE\n"
                    sql_query_end += f"{tabs}{target}[{index}] := {item[1]};\n"
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
