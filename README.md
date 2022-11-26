# function-trees
used to solve different calculus problems (currently only derivatives) and simplify functions.

you make a function by combining nodes (parser not made yet) to make trees. Currently the only nodes are:
NumNode(n) = a number n
VarNode("x") = a variable with name "x"
AddNode(left, right) = left + right
SubNode(left, right) = left - right
MultNode(left, right) = left * right
DivNode(left, right) = left / right
PowNode(left, right) = left ^ right
LogNode(left, right) = log base left of right
SinNode(f(x)) = sin(f(x))
CosNode(f(x)) = cos(f(x))

There is a nthroot(a, n) function that returns PowNode(a, 1/n)

e.g. if i had the function x^2, which would be represented as PowNode(VarNode("x"), NumNode(2)). Then if i called f.derivative() it would return 2*(x^(2-1)) but if you do f.derivative().simplify() then it would give 2 * x. the solve(vars) function where vars is a dictionary solves f(a,b,...) when a,b,.. are replaced with the value of vars[var_name].

warning: the simplify() function isn't perfect
