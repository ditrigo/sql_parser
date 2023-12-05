from pyparser import pyparser, replace_variables
from datetime import datetime
import re
import ast

s_1200_4 = 1
s_1500_4 = 2
s_1530_4 = 3
d = 4
e = datetime(2021,10,5,21,40)
f = datetime.today()
s_2110_4 = 20
s_2110_5 = 10
bankruptcy_procedure = ""
bankruptcy_procedure_bool = 1
tax_burden = 5
ru_tax_burden = 10
subsidy_sum = 56
sr_chis_thisyear = 10
sr_chis_lastyear = -100
postup_lastyear = 10
postup_thisyear = 10
bznaper_lastyear = 10
bznaper_thisyear = 20
clr = 10
dolg = 26000000
dolg_overdue = 4
force = 9.99
start_ball = "микро"

expression = 'условие(ПОИСК("ликв";imported_attributes.status_egrn) or ПОИСК("исключ";imported_attributes.status_egrn);-140;условие(ПОИСК("действ";imported_attributes.status_egrn);0;-35))'
expression = pyparser(expression)
print(expression)

try:
    ast.parse(expression)
    print('OK syntax')
    # expression = print(eval(expression))
except Exception as e:
    print(f"Error in function: {e}")
# print(replace_variables(expression, imported_attr))

# try:
#     print("OK eval")
#     result = eval(expression)
#     print(result)
# except Exception as e:
#     print(f"Error in eval: {e}") 
