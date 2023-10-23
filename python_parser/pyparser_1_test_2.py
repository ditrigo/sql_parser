import re

def transform_if_else(input_string):
    if_pattern = r'если\('
    then_pattern = r', то'
    else_pattern = r', иначе'

    if_matches = [match.start() for match in re.finditer(if_pattern, input_string)]
    then_matches = [match.start() for match in re.finditer(then_pattern, input_string)]
    else_matches = [match.start() for match in re.finditer(else_pattern, input_string)]
    print("Matches: ", if_matches, then_matches, else_matches)

    i_range = len(if_matches)

    for i in range(i_range):

        print("+")
        first_if = min(if_matches)
        last_then = max(then_matches)
        last_else = max(else_matches)
        print("\tMin else: ", first_if, "\n\tMax thes: ", last_then, "\n\tMax else: ", last_else)

        # if_matches.pop(0)
        # then_matches.pop(-1)
        # else_matches.pop(-1)
        # print("Matches: ", if_matches, then_matches, else_matches)

        modified_string = input_string[:first_if] + '(' + input_string[last_then+len(', то '):last_else] + ' if ' + input_string[first_if+len('если('):last_then] + ' else ' + input_string[last_else+len(', иначе '):-1] + ')'
        print("str: ", modified_string)

        if_matches = [match.start() for match in re.finditer(if_pattern, modified_string)]
        then_matches = [match.start() for match in re.finditer(then_pattern, modified_string)]
        else_matches = [match.start() for match in re.finditer(else_pattern, modified_string)]

        

    return modified_string


# Пример использования:
input_string = 'если(если(2_a + 2_b > 2_c, то 2_d, иначе 2_e) + 1_b < 1_c, то 1_d, иначе 1_e)'
transformed_string = transform_if_else(input_string)

print("Преобразованная строка:")
print(transformed_string)
