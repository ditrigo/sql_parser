import re

def replace_contains(text):
    pattern = r'(\w+)\s+содержит\s+"(\w+)"'
    replacement = r'"\2" in \1'
    result = re.sub(pattern, replacement, text)
    return result

# Пример использования
original_string = 'условие(dolg содержит "конк" and i<7; -10; 0)'
modified_string = replace_contains(original_string)
print(modified_string)