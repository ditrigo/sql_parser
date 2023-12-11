import re

def process_strings(expression, expression_second=None):

    stripped_string = re.sub(r'(\w+\.)', '', expression)

    variable_names = re.findall(r'\b(\w+)\b', expression)

    restored_string = expression
    for i in range(1, len(variable_names), 2):
        original_var = variable_names[i]
        stripped_var_name = re.sub(r'(\w+\.)', '', original_var)
        new_var_name = f'{variable_names[i-1]}.{original_var}'
        
        pattern = r'(?<!\.)\b' + re.escape(original_var) + r'\b'
        
        if expression_second is not None:
            expression_second = re.sub(pattern, new_var_name, expression_second)
        
        restored_string = re.sub(r'\b' + original_var + r'\b', stripped_var_name, restored_string)

    if expression_second is not None:
        return restored_string, expression_second
    else:
        return stripped_string

input_result = process_strings("imported_attributes.dolg/(counted_attributes.dolg_in_balance+imported_attributes.dolg)")
print("\nРезультат обработки input_string:", input_result)

input_result, second_result = process_strings("imported_attributes.dolg/(counted_attributes.dolg_in_balance+imported_attributes.dolg)", "dolg_in_balance+dolg")
print("\nРезультат обработки input_string:", input_result)
print("Результат обработки second_string:", second_result)
