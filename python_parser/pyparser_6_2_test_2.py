def generate_condition_string(lst):
    result = ""
    add_before = ""
    i = 0
    while i < len(lst):
        
        if lst[i] == "cond":
            cond = generate_condition_string(lst[i+1])
            res1 = generate_condition_string(lst[i+3])
            res2 = generate_condition_string(lst[i+5])
            result += f"({res1} if {cond} else {res2})"
            add_before = ""
            i += 6
        elif isinstance(lst[i], list):
            result += generate_condition_string(lst[i])
            i += 1
        else:
            if lst[i] == "add_before" or lst[i] == "add_after":
                add_before = lst[i+1]
                result += str(lst[i+1])
                i += 2
            else:
                result += str(lst[i])
                i += 1
    return result

original_list = ['cond', ['add_before', 'a + ', 'cond', 'вклад>300', 'res1', '5', 'res2', ['cond', 'выручка>123', 'res1', '333', 'res2', '444'], 'add_after', ' + b>100'], 'res1', '2', 'res2', '10']

result_string = generate_condition_string(original_list)
print(result_string)
