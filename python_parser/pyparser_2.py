def parse_condition(s):
    # Разделяем условие на левую и правую часть
    left, right = s.split(">")
    
    # Если правая часть является числом, то возвращаем ее как целое число
    try:
        return int(right)
    except ValueError:
        pass
    
    # Иначе разбираем правое выражение на операторы
    op, value = right.split()[0], right.split()[1:]
    
    # Если оператор - это сложение, то выполняем его
    if op == "+":
        result = sum([int(v) for v in value])
    elif op == "-":
        result = sum([-int(v) for v in value])
    else:
        raise SyntaxError("Unsupported operator {}".format(op))
        
    return result

def translate_if(s):
    condition, then_, else_ = s.split(", ")
    condition = parse_condition(condition)
    then_ = translate_if(then_) if "," in then_ else then_.strip()
    else_ = translate_if(else_) if "," in else_ else else_.strip()
    return f"{condition} if {then_} else {else_}"

# Примеры использования
print(translate_if("a > b, a+b, c"))
print(translate_if("a > b, a+b, c, d > e, f+g")) # Output: ((a > b) if (a + b) else c) and (d > e) if (f + g) else None