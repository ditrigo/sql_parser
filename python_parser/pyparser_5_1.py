# def parse_condition(s):
#     condition_start = s.find('(')
#     condition_end = s.rfind(')')
#     return s[condition_start+1:condition_end]

# def parse_result1(s):
#     result1_start = s.find(',')
#     result1_end = s.rfind(',')
#     return s[result1_start+1:result1_end]

# def parse_result2(s):
#     result2_start = s.rfind(',')
#     result2_end = len(s) - 1
#     return s[result2_start+1:result2_end]

# def parse_structure(s):
#     condition = parse_condition(s)
#     result1 = parse_result1(s)
#     result2 = parse_result2(s)
    
#     result = f"{result1} if {condition} else {result2}"
#     return result

def convert_to_python_code(s):
    i = 0
    result = ""

    while i < len(s):
        if s[i:i+8] == "условие(":
            condition_start = i
            count = 1
            i += 8
            while count > 0:
                if s[i] == '(':
                    count += 1
                elif s[i] == ')':
                    count -= 1
                i += 1
            condition_end = i

            result1_start = i
            count = 1
            while count > 0:
                if s[i] == '(':
                    count += 1
                elif s[i] == ')':
                    count -= 1
                i += 1
            result1_end = i

            result2_start = i
            count = 1
            while count > 0:
                if s[i] == '(':
                    count += 1
                elif s[i] == ')':
                    count -= 1
                i += 1
            result2_end = i

            structure_end = i

            condition = s[condition_start:condition_end]
            result1 = s[result1_start:result1_end]
            result2 = s[result2_start:result2_end]

            result += f"{result1} if {condition} else {result2}"

        else:
            result += s[i]
            i += 1

    return result

s = "условие(сальдо>100, 0, условие(вклад>300, 11, 12)) + условие(кредит<200, 5, 7)"
result = convert_to_python_code(s)
print(result)
