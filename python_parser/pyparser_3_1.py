import re

def swap_if_then_else(input_str):
    # Используем регулярное выражение для поиска самого внешнего вхождения шаблона (if ... then ... else ...)
    pattern = r'\(if(.*?)then(.*?)else(.*?)\)'
    match = re.search(pattern, input_str)

    if match:
        # Заменяем 'if' на 'then' и наоборот только в самом внешнем вхождении
        swapped_match = f'(then{match.group(2)}if{match.group(1)}else{match.group(3)})'
        # Заменяем оригинальное вхождение на модифицированное
        input_str = input_str[:match.start()] + swapped_match + input_str[match.end():]

        # Рекурсивно вызываем функцию для замены внутренних вхождений
        input_str = swap_if_then_else(swapped_match)

    return input_str

# Пример использования
input_str = "(if (if x + y == z then q else r) > b then x else (if c < d then y else z)) + (if e < f then g else h)"
output_str = swap_if_then_else(input_str)
print(output_str)
