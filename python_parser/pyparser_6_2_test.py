def construct_expression(lst, add_before='', cond='', res1='', res2='', add_after=''):
    print("+")
    result = ""
    for item in lst:
        # if isinstance(item, list):
        #     result += construct_expression(item, add_before, cond, res1, res2, add_after)
        if isinstance(item, str):
            if lst.index(item) + 1 < len(lst) and isinstance(lst[lst.index(item) + 1], str):
                if item == 'add_before':
                    add_before = lst[lst.index(item) + 1]
                if item == 'cond':
                    cond = lst[lst.index(item) + 1]
                if item == 'res1':
                    res1 = lst[lst.index(item) + 1]
                if item == 'res2':
                    res2 = lst[lst.index(item) + 1]
                if item == 'add_after':
                    add_after = lst[lst.index(item) + 1]
            else:
                if item == 'add_before':
                    add_before = construct_expression(item, add_before, cond, res1, res2, add_after)
                if item == 'cond':
                    cond = construct_expression(item, add_before, cond, res1, res2, add_after)
                if item == 'res1':
                    res1 = construct_expression(item, add_before, cond, res1, res2, add_after)
                if item == 'res2':
                    res2 = construct_expression(item, add_before, cond, res1, res2, add_after)
                if item == 'add_after':
                    add_after = construct_expression(item, add_before, cond, res1, res2, add_after)
    result += f"{add_before} ({res1} if {cond} else {res2}) {add_after}"
    return result

lst = ['cond', ['add_before', 'a + ', 'cond', 'вклад>300', 'res1', '5', 'res2', ['cond', 'выручка>123', 'res1', '333', 'res2', '444'], 'add_after', ' + b>100'], 'res1', '2', 'res2', '10']

expression = construct_expression(lst)

print(expression)
