def split_condition_string(condition_string):
    result = []
    counter = 0
    current_token = ''
    
    index = 0
    while index < len(condition_string):
        if condition_string[index:index+8] == 'условие(':
            counter = 0
            result.append('condition')
            current_token = ''
            index += 8
        elif condition_string[index] == ',':
            if counter == 1:
                result.append('result1')
            elif counter == 2:
                result.append('result2')
            counter += 1
            result.append(current_token)  # Добавляем текущий токен
            current_token = ''
            index += 1
        else:
            current_token += condition_string[index]
            index += 1
    
    # Добавляем оставшийся токен после последней запятой
    if current_token:
        if counter == 0:
            result.append('result1')
        elif counter == 1:
            result.append('result2')
        result.append(current_token)
            
    return result

condition_string = "условие(сальдо>100, 0, условие(вклад>300, 11, 12)) + условие(кредит<200, 5, 7)"
result = split_condition_string(condition_string)
print(result)
