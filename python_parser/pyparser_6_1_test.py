def construct_string(lst):
    result = ""

    for i, item in enumerate(lst):
        if isinstance(item, list):
            result += construct_string(item)
        elif isinstance(item, str):
            if len(lst) == 3:
                cond = lst[0]
                res1 = lst[1]
                res2 = lst[2]
                result += f"(res1)"

    return result

# Пример списка
lst = [['a + ', 'вклад>300', '5', ['выручка>123', '333', '444'], ' + b>100'], '2', '10']

# Генерируем строку
expression = construct_string(lst)

print(expression)
