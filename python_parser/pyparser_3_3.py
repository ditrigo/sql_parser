def find_matching_parentheses(s):
    count = 0
    for i, char in enumerate(s):
        if char == '(':
            count += 1
        elif char == ')':
            count -= 1
            if count == 0:
                return i
    return -1

def parse_condition(expression):
    condition = [] 
    result1 = ""
    result2 = ""
    index = 0
    expr_list = []
    print("+", expression)
    while(expression != ""):
        start_if = expression.find("if")
        print(start_if)
        end_if = find_matching_parentheses(expression)
        condition.append(expression[start_if-1:end_if+1])
        expression = expression[end_if+1:]
        print("+")



    

    return condition, result1, result2, expr_list

# Пример использования
expression = "(if (if x + y == z then q else r) > b then x else (if c < d then y else z)) + (if e < f then g else h)"
condition, result1, result2, expr_list = parse_condition(expression)

# print(f"Индекс: {0}")
print(f"\nУсловие 1: {condition}")
print(f"Результат 1: {result1}")
print(f"Результат 2: {result2}")
print(f"Expr_list: {expr_list}")

list = []
nlist = [[['a'], 'b'], 'c']
list = ['x', 'y', nlist]
print(list[2][0])