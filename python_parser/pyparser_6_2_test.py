# pyparser_6_1.py copy

def pyparser(str):
    if not str:
        return []
    res = []
    i = 0
    cond_counter = 0
    res_counter = 0
    while i<len(str):

        if str[i] == "у" and str[i:i+8] == "условие(":

            if cond_counter == 0: 
                cond_start = i+8

                if str[0:i] != '':
                    res.append("add_before")
                    res.append(str[0:i])
            
            cond_counter += 1
            i += 7

        elif str[i] == ")":

            if cond_counter == 1:
                res2_end = i
                result_1 = pyparser(str[res2_start:res2_end])

                res.append("res2")
                res.append(result_1)

                
                if str[i+1:] != '':
                    res.append("add_after")
                    res.append(str[i+1:])

            cond_counter -= 1

        elif str[i] == ";" and cond_counter == 1:
            if res_counter == 0:
                res_counter += 1
                cond_end = i
                res1_start = i+1
                result_1 = pyparser(str[cond_start:cond_end])

                res.append("cond")
                res.append(result_1)
                
            elif res_counter == 1:
                res_counter = 0
                res1_end = i
                res2_start = i+1
                result_1 = pyparser(str[res1_start:res1_end])

                res.append("res1")
                res.append(result_1)
            
        i += 1

    if res == []:
        return str
    else:
        return res


expression = "условие(a + условие(вклад>300;5;условие(выручка>123;333;444)) + b>100;2;10)"
result = pyparser(expression)
print(result)