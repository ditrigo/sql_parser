def assign_numbers(expression):
    counter = 1
    result = ""
    stack = []

    for char in expression:
        if char == "(":
            if stack and stack[-1] == "if":
                result += str(counter)
                counter += 1
            stack.append(char)
        elif char == ")":
            if stack and stack[-1] == "if":
                result += str(counter)
                counter += 1
            stack.pop()
            result += char
        else:
            result += char
            if char == "f":
                stack.append("if")

    return result

expression = "(if (if x + y == z then q else r) > b then x else (if c < d then y else z)) + (if e < f then g else h)"
result = assign_numbers(expression)
print(result)
