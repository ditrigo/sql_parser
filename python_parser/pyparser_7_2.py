from pyparser import pyparser, replace_variables
from datetime import datetime
s_1200_4 = 1
s_1500_4 = 2
s_1530_4 = 3
d = 4
e = '2023-11-07 21:41'
f = datetime.today().year

expression = 'условие((s_1500_4-s_1530_4)=0;условие(s_1200_4>0;20;0);условие(И(s_1200_4/(s_1500_4-s_1530_4)>1;s_1200_4/(s_1500_4-s_1530_4)<3);20;0))'
expression = pyparser(expression)
print(expression)
print(eval(expression))
# print(replace_variables(expression, imported_attr))


if formula.startswith("Error"):
    list_markers.append({'Error': formula, 'value': "Error"})
else:
    try:
        list_markers.append({'formula': formula, 'value': eval(formula)})
    except Exception as e:
        list_markers.append({'formula': formula, 'value': e})