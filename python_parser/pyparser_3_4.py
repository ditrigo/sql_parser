def parse_condition_string(condition_str):
    stack = []
    current = {"condition": None, "result1": None, "result2": None}
    result = []

    for char in condition_str:
        if char == '(':
            stack.append(current)
            current = {"condition": None, "result1": None, "result2": None}
        elif char == ')':
            parent = stack.pop()
            if parent["condition"] is None:
                parent["condition"] = current
            elif parent["result1"] is None:
                parent["result1"] = current
            else:
                parent["result2"] = current
            current = parent
        elif char == ',':
            stack[-1]["condition"] = current
            current = {"condition": None, "result1": None, "result2": None}
        else:
            current = {"condition": char, "result1": None, "result2": None}
            if not stack:
                result.append(current)

    return result

def evaluate_condition(condition):
    if isinstance(condition, dict):
        return evaluate_condition(condition["condition"]) + \
               evaluate_condition(condition["result1"]) + \
               evaluate_condition(condition["result2"])
    else:
        return [condition]

condition_str = "условие(сальдо>100, 0, условие(вклад>300, 11, 12)) + условие(кредит<200, 5, 7)"
conditions = parse_condition_string(condition_str)
results = evaluate_condition(conditions)

print(results)
