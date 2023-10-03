from sys import argv
import regex as re


def parse_query(query):
    # Разбиваем запрос на отдельные условия
    conditions = query.split(' + ')
    # Создаем список для хранения значений
    values = []
    # Создаем список для хранения условий
    conditions_list = []
    # Проходимся по каждому условию
    for condition in conditions:
        # Разбиваем условие на три части: условие, значение при True и значение при False
        condition = condition.split(',')
        # Удаляем лишние пробелы
        condition = condition.strip()
        true_value = true_value.strip()
        false_value = false_value.strip()
        # Добавляем значения в список
        values.append((true_value, false_value))
        # Добавляем условие в список
        conditions_list.append(condition)
    # Формируем новый код
    new_code = "DECLARE\n"
    for i, condition in enumerate(conditions_list):
        new_code += f"    v_temp{i} INTEGER;\n"
    new_code += "BEGIN\n"
    for i, condition in enumerate(conditions_list):
        new_code += f"    IF {condition} THEN\n"
        new_code += f"        v_temp{i} := {values[i][0]};\n"
        new_code += f"    ELSE\n"
        new_code += f"        v_temp{i} := {values[i][1]};\n"
        new_code += f"    END IF;\n"
    new_code += "    v_rate := "
    for i in range(len(conditions_list)):
        new_code += f"v_temp{i} + "
    new_code = new_code[:-3] + ";\n"
    new_code += "END;"
    return new_code


if __name__ == '__main__':
    contents = open(argv[1], 'r').read()
    lst = parse_query(contents)

    print(lst)

    with open('generated_query.sql', 'w', encoding='utf-8-sig') as f:
        f.write(lst)
