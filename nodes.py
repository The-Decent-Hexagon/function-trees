import math

e = "e"

class NumNode:
    def __init__(self, val):
        self.val = val

    def derivative(self):
        return NumNode(0)

    def sub(self, num):
        return NumNode(self.val - num.val)

    def simplify(self):
        return self

    def solve(self, vars):
        return self.val

    def __eq__(self, other):
        if(type(other) == NumNode):
            return self.val == other.val
        return False

    def __repr__(self):
        return f"{self.val}"

class VarNode:
    def __init__(self, name):
        self.name = name

    def derivative(self):
        return NumNode(1)

    def simplify(self):
        return self

    def solve(self, vars):
        return vars[self.name]

    def __eq__(self, other):
        if(type(other) != VarNode): return False
        return self.name == other.name

    def __repr__(self):
        return f"{self.name}"

class AddNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def derivative(self):
        return AddNode(self.left.derivative(), self.right.derivative())

    def simplify(self):
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        if(type(self.left) == NumNode and type(self.right) == NumNode):
            return NumNode(self.left.val + self.right.val)

        if (type(self.left) == NumNode and self.left.val == 0):
            return self.right
        elif (type(self.right) == NumNode and self.right.val == 0):
            return self.left

        return self

    def solve(self, vars):
        left = self.left.solve(vars)
        right = self.right.solve(vars)

        return left + right

    def __eq__(self, other):
        if(type(other) in [NumNode, VarNode]): return False
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        return f"({self.left} + {self.right})"

class SubNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def derivative(self):
        return SubNode(self.left.derivative(), self.right.derivative())

    def simplify(self):
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        if(self.left == self.right):
            return NumNode(0)

        if(type(self.left) == NumNode and type(self.right) == NumNode):
            return NumNode(self.left.val - self.right.val)

        if(self.left == NumNode(0)):
            if(type(self.right) == SubNode and self.right.left == NumNode(0)):
                return self.right.right

        if(type(self.right) == NumNode and self.right.val == 0):
            return self.left

        return self

    def solve(self, vars):
        left = self.left.solve(vars)
        right = self.right.solve(vars)

        return left - right

    def __eq__(self, other):
        if(type(other) in [NumNode, VarNode]): return False
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        if(self.left == NumNode(0)):
            return f"-({self.right})"
        return f"({self.left} - {self.right})"

class MultNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def derivative(self):
        return AddNode(MultNode(self.left, self.right.derivative()), MultNode(self.left.derivative(), self.right))

    def simplify(self):
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        if(type(self.left) == DivNode):
            if self.left.right == self.right:
                return self.left.left

        if(type(self.right) == DivNode):
            if self.right.right == self.left:
                return self.right.left

        if(type(self.left) == NumNode and type(self.right) == NumNode):
            return NumNode(self.left.val * self.right.val)
        elif(type(self.left) == NumNode and type(self.right) == VarNode):
            if self.left.val == 0:
                return NumNode(0)
            elif self.left.val == 1:
                return VarNode(self.right.name)
        elif(type(self.left) == VarNode and type(self.right) == NumNode):
            if self.right.val == 0:
                return NumNode(0)
            elif self.right.val == 1:
                return VarNode(self.left.name)

        if(type(self.left) == NumNode and self.left.val == 1):
            return self.right
        elif(type(self.right) == NumNode and self.right.val == 1):
            return self.left

        if (type(self.left) == NumNode and self.left.val == 0):
            return NumNode(0)
        elif (type(self.right) == NumNode and self.right.val == 0):
            return NumNode(0)

        return self

    def solve(self, vars):
        left = self.left.solve(vars)
        right = self.right.solve(vars)

        return left * right

    def __eq__(self, other):
        if(type(other) in [NumNode, VarNode]): return False
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        return f"({self.left} * {self.right})"

class DivNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def derivative(self):
        return DivNode(SubNode(MultNode(self.right, self.left.derivative()), MultNode(self.left, self.right.derivative())), PowNode(self.right, NumNode(2)))

    def simplify(self):
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        if(self.left == self.right):
            return NumNode(1)

        if (type(self.left) == MultNode and type(self.right) == MultNode):
            if (self.left.left == self.right.left):
                return DivNode(self.left.right, self.right.right).simplify()
            if (self.left.left == self.right.right):
                return DivNode(self.left.right, self.right.left).simplify()
            if (self.left.right == self.right.left):
                return DivNode(self.left.left, self.right.right).simplify()
            if (self.left.right == self.right.right):
                return DivNode(self.left.left, self.right.left).simplify()

        if(type(self.left) == PowNode and type(self.right) == PowNode):
            if(self.left.left == self.right.left):
                return PowNode(self.left.left, SubNode(self.left.right, self.right.right)).simplify()

        if(type(self.left) == MultNode):
            if(self.left.left == self.right):
                return self.left.right
            if(self.left.right == self.right):
                return self.left.left

        if (type(self.right) == MultNode):
            if (self.right.left == self.left):
                return self.right.right
            if (self.right.right == self.left):
                return self.right.left

        if(type(self.left) == NumNode and type(self.right) == NumNode):
            return NumNode(self.left.val / self.right.val)
        elif(type(self.left) == VarNode and type(self.right) == NumNode):
            if self.right.val == 1:
                return VarNode(self.left.name)

        if (type(self.left) == NumNode and self.left.val == 0):
            return NumNode(0)

        return self

    def __eq__(self, other):
        if(type(other) in [NumNode, VarNode]): return False
        return self.left == other.left and self.right == other.right

    def solve(self, vars):
        left = self.left.solve(vars)
        right = self.right.solve(vars)

        return left / right

    def __repr__(self):
        return f"({self.left} / {self.right})"

class PowNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def derivative(self):
        if(type(self.left) == NumNode and type(self.right) == NumNode): return NumNode(0) # not needed but for speed and simplification
        if(type(self.left) == VarNode and type(self.right) == VarNode): return MultNode(PowNode(VarNode(self.left.name), VarNode(self.left.name)), AddNode(NumNode(1), LogNode(e, VarNode(self.left.name)))) # not needed but for speed and simplification
        if(type(self.left) == VarNode and type(self.right) == NumNode): return MultNode(self.right, PowNode(self.left, SubNode(self.right, NumNode(1)))) # not needed but for speed and simplification
        if(type(self.left) == NumNode and type(self.right) == VarNode): return MultNode(self, LogNode(e, self.left)) # not needed but for speed and simplification
        if(type(self.right) == NumNode): return MultNode(MultNode(self.right, PowNode(self.left, SubNode(self.right, NumNode(1)))), self.left.derivative()) # not needed but for speed and simplification
        if(type(self.left) == NumNode): return MultNode(MultNode(LogNode(e, self.left), self), self.right.derivative())
        return MultNode(PowNode(self.left, SubNode(self.right, NumNode(1))),
        AddNode(MultNode(self.right, self.left.derivative()),
        MultNode(self.left, MultNode(LogNode(e, self.left), self.right.derivative()))))

    def simplify(self):
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        if (type(self.left) == NumNode and type(self.right) == NumNode):
            return NumNode(self.left.val ** self.right.val)
        elif (type(self.left) == VarNode and type(self.right) == NumNode):
            if self.right.val == 0:
                return NumNode(1)
            elif self.right.val == 1:
                return VarNode(self.left.name)
        elif(type(self.left) == NumNode and type(self.right) == VarNode):
            if(self.left.val == 0):
                return NumNode(0)
            elif(self.left.val == 1):
                return NumNode(1)
        return self

    def solve(self, vars):
        left = self.left.solve(vars)
        right = self.right.solve(vars)

        return left ** right

    def __eq__(self, other):
        if(type(other) in [NumNode, VarNode, str]): return False
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        return f"({self.left} ^ {self.right})"

class LogNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        if(type(self.left) != str):
            self.left = self.left.simplify()
        if (type(self.right) != str):
            self.right = self.right.simplify()

        if(type(self.left) in [NumNode, str] and type(self.right) in [NumNode, str]):
            if(self.left == "e"):
                if(self.right == "e"):
                    return NumNode(1)
                return NumNode(math.log(self.right.val))

            if(self.right == "e"):
                return NumNode(math.log(math.e, self.left.val))

            return NumNode(math.log(self.right.val, self.left.val))

        return self

    def derivative(self):
        if(type(self.left) in [NumNode, str]):
            return DivNode(self.right.derivative(), MultNode(self.right, LogNode(e, self.left)))

        return DivNode(LogNode(e, self.right), LogNode(e, self.left)).derivative()

    def solve(self, vars):
        left = self.left.solve(vars)
        right = self.right.solve(vars)

        return math.log(right, left)

    def __eq__(self, other):
        if(type(other) in [NumNode, VarNode, str]): return False
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        if(self.left == "e"):
            if(str(self.right).startswith("(") and str(self.right).endswith(")")):
                return f"log{self.right}"
            return f"log({self.right})"
        return f"(Log base {self.left} of {self.right})"

class SinNode:
    def __init__(self, node):
        self.node = node

    def simplify(self):
        self.node = self.node.simplify()
        return self

    def derivative(self):
        return MultNode(CosNode(self.node), self.node.derivative())

    def solve(self, vars):
        node = self.node.solve(vars)

        return math.sin(node)

    def __repr__(self):
        return f"sin{self.node}"

class CosNode:
    def __init__(self, node):
        self.node = node

    def simplify(self):
        self.node = self.node.simplify()
        return self

    def derivative(self):
        return MultNode(SubNode(NumNode(0), SinNode(self.node)), self.node.derivative())

    def solve(self, vars):
        node = self.node.solve(vars)

        return math.cos(node)

    def __repr__(self):
        return f"cos{self.node}"

def nthroot(a, n):
    return PowNode(a, NumNode(1/n.val))