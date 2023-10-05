def items_to_string(items):
    temp = ""
    str = ""
    result = ""
    temp = ""
    prev_item = None

    for item in items:

        if item[0] == 'condition':
            i=0
        
        elif item[0] == 'word':     
            temp += f"{item[1]}"
            prev_item = 'word'
            # else:
            #     temp = "IF"

        elif item[0] == 'delin':  # +-*/
            temp += f"{item[1]}"
            prev_item = 'delin'

        elif item[0] == 'comparison':  # <>=
            temp += f"{item[1]}"
            prev_item = 'comparison'

        elif item[0] == 'number':   # 123
            if prev_item == 'comparison':
                temp += f"{item[1]} THEN\n"
            elif prev_item == 'number':
                temp += "ELSE\n"
            temp += f"{item[1]};\n"
            prev_item = 'number'

        elif item[0] == 'paren':   # () 
            if item[1] == '(':
                temp = "IF"           
            if item[1] == ')':
                result += temp
                temp = ""
            prev_item = 'paren'


    str += result    
    return str

items = [('word', 'условие'), ('paren', '('), ('word', 'сальдо'), ('delin', '+'), ('word', 'условие'), ('paren', '('), ('word', 'вклад'), ('comparison', '>'), ('number', '300'), ('number', '5'), ('word', 'условие'), ('paren', '('), ('word', 'выручка'), ('comparison', '>'), ('number', '123'), ('number', '333'), ('number', '444'), ('paren', ')'), ('paren', ')'), ('comparison', '>'), ('number', '100'), ('number', '2'), ('number', '10'), ('paren', ')')]

temp_string = items_to_string(items)
print(temp_string)
