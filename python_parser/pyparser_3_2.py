def evaluate(expression, variables):
    def eval_condition(condition, variables):
        if '==' in condition:
            left, right = condition.split('==')
            return variables[left.strip()] == variables[right.strip()]
        elif '<' in condition:
            left, right = condition.split('<')
            return variables[left.strip()] < variables[right.strip()]
        elif '>' in condition:
            left, right = condition.split('>')
            return variables[left.strip()] > variables[right.strip()]

    def eval_expression(expression, variables):
        if expression.startswith('if'):
            condition_start = expression.find('(')
            condition_end = expression.rfind(')')
            true_value_start = expression.find('then') + len('then')
            true_value_end = expression.find('else')

            condition = expression[condition_start+1:condition_end].strip()
            true_value = expression[true_value_start:true_value_end].strip()
            false_value = expression[true_value_end+len('else'):].strip()

            if eval_condition(condition, variables):
                return eval_expression(true_value, variables)
            else:
                return eval_expression(false_value, variables)
        elif '+' in expression:
            terms = expression.split('+')
            return sum(eval_expression(term, variables) for term in terms)
        elif '-' in expression:
            left, right = expression.split('-')
            return eval_expression(left, variables) - eval_expression(right, variables)
        elif '*' in expression:
            left, right = expression.split('*')
            return eval_expression(left, variables) * eval_expression(right, variables)
        elif '/' in expression:
            left, right = expression.split('/')
            return eval_expression(left, variables) / eval_expression(right, variables)
        else:
            return variables[expression.strip()]

    return eval_expression(expression, variables)

# Пример выражения
expression = "(if (if x + y == z then q else r) > b then x else (if c < d then y else z)) + (if e < f then g else h)"

# Переменные
variables = {'x': 5, 'y': 3, 'z': 8, 'q': 10, 'r': 20, 'b': 15, 'c': 2, 'd': 4, 'e': 1, 'f': 7, 'g': 6, 'h': 9}

# Оценка выражения
result = evaluate(expression, variables)
print(result)
