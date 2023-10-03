import re

def split_expression(input_string):
    operators = r'\s*[-+*/]\s*'
    matches = re.split(operators, input_string)
    return matches

input_string = "условие(сальдо>100, 2, условие(вклад>300, 5, 6)) + условие(кредит>200, 7, 9)"
parts = split_expression(input_string)

print(parts)
