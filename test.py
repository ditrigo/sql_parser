from sympy import sympify

expression = "(a+b)/c + n/(m+p) + a/(b+c/d)"

expr = sympify(expression)

denominators = [term.as_numer_denom()[1] for term in expr.as_ordered_terms()]

print(denominators)
