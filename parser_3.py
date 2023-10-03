import re

def parse_condition(input_string, indent_level=1):
    input_string = input_string.replace('условие(', 'IF ')
    input_string = input_string.replace(',', ' THEN\n' + '\t' * indent_level, 1)  # Заменяем первую запятую на THEN
    input_string = re.sub(r',', r' ELSE\n' + '\t' * indent_level, input_string)  # Заменяем все остальные запятые на ELSE
    input_string = input_string.replace(')', ';\n' + '\t' * indent_level + 'END IF')
    return input_string

def convert_to_plpgsql(input_string):
    output_string = ''
    
    def parse_recursive(input_string, indent_level=1):
        nonlocal output_string
        conditions = re.findall(r'условие\((.*?)\)', input_string)
        for i, condition in enumerate(conditions):
            converted_condition = parse_condition(condition, indent_level=indent_level+1)
            output_string += converted_condition
            
            if 'условие(' in condition:
                print(condition)
                parse_recursive(condition, indent_level=indent_level+1)
    
    parse_recursive(input_string)
    return output_string

input_string = "условие(сальдо>100, 2, условие(вклад>300, 5, 6)) + условие(кредит>200, 7, 9)"
output_string = convert_to_plpgsql(input_string)
print("---------------------------")
print(output_string)
