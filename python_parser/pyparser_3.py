def replace_conditions(input_string):
    replaced_string = input_string.replace("если(", "(if ").replace(", то", " then").replace(", иначе", " else")
    return replaced_string

# Пример использования
original_string = 'если(a > b, то x, иначе если(c < d, то y, иначе z))'
new_string = replace_conditions(original_string)

print(new_string)