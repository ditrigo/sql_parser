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
# dolg = 26000000
dolg_overdue = 4
force = 9.99
start_ball = "микро"
empty_item = 1

a = 5
b = 0

debit = 10
credit = 20
payment = "str"

expression = 'условие(ЕСЛИОШИБКА(imported_attributes.dolg/(counted_attributes.dolg_in_balance+imported_attributes.dolg);imported_attributes.dolg*5)>20;10;0)'
expression = pyparser(expression)
print(expression)

try:
    ast.parse(expression)
    print('OK syntax')
    # eval(expression)
except TypeError as e:
    print(f"Неподдерживаемая операция для этого типа данных")
except Exception as e:
    print(f"Error in function: {e}")
# print(replace_variables(expression, imported_attr))

# try:
#     print("OK eval")
#     result = eval(expression)
#     print(result)
# except Exception as e:
#     print(f"Error in eval: {e}") 

