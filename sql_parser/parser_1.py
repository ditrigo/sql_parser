from sys import argv
import regex as re


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
                print(token)
                token = re.sub(r"[^-0-9]", "", token)
                print(token)
                items.append(("number", token))

        nLines.append(items)

    return nLines


def generate_sql_query(data):

    inn = 23445667
    sql_query = "CREATE FUNCTION if EXISTS f_rate()\nRETURNS INTEGER\nLANGUAGE PLPGSQL\nAS\n$$\n"  # noqa: E501
    
    sql_query += "\tDECLARE\n\t\tv_rate INTEGER;\n\t\tv_origin varchar(255);\n\t\tv_value INTEGER;\n\tBEGIN\n"

    sql_query += "\tEXECUTE \"SELECT origin FROM main_catalog_fileds WHERE filed_name LIKE \"|| <filed_name (сальдо)> into v_origin;\n"
    sql_query += f"\tEXECUTE \"SELECT\" || v_origin || \"FROM csv_attributes WHERE inn LIKE\" || <inn ({inn})> into v_value;\n"

    target = "v_rate"
    end = ""
    tabs = "\t\t"

    prev_type = None

    for sublist in data:

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
                sql_query += f"{tabs}{target} := {item[1]};\n"
                prev_type = 'number'
        
        if sublist != data[-1]:
            sql_query += f"{tabs}ELSE\n"
        
    sql_query += f"{tabs}{end}\nEND;\n$$;"
    sql_query += f"return v_rate"
    return sql_query


def parser(str):
    
    lst = lexer(str)
    sql_query = generate_sql_query(lst)

    return sql_query


if __name__ == '__main__':
    contents = open(argv[1], 'r').read()
    lst = parser(contents)

    print(lst)

    with open('generated_query.sql', 'w', encoding='utf-8-sig') as f:
        f.write(lst)
