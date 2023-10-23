import re

def convert_formula_to_python(formula):
    # Паттерн для поиска условий в формуле
    pattern = r'если\(([^,]+), то ([^,]+), иначе ([^\)]+)\)'
    print("+")
    # Функция для обработки условий
    def process_condition(match):
        condition, true_value, false_value = match.groups()
        print(match.groups())
        return f'({true_value} if {condition} else {false_value})'

    # Рекурсивно обрабатываем вложенные условия
    python_formula = re.sub(pattern, process_condition, formula)
    python_formula = re.sub(pattern, process_condition, python_formula)
    return python_formula

# Пример использования
formula = 'если(если(k + l = m, то q, иначе w) + y < z, то a, иначе b)'
python_formula = convert_formula_to_python(formula)
print(python_formula)  # Выведет "(a if x + y < z else (c if m > n else d))"
