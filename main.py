import re

class Context:
    def __init__(self):
        self.variables = {}

    def set_variable(self, variable, value):
        self.variables[variable] = value

    def get_variable(self, variable):
        return self.variables.get(variable, 0)


class AbstractExpression:
    def interpret(self, context):
        pass


class Number(AbstractExpression):
    def __init__(self, value):
        self.value = value

    def interpret(self, context):
        return self.value


class Variable(AbstractExpression):
    def __init__(self, name):
        self.name = name

    def interpret(self, context):
        return context.get_variable(self.name)


class AddExpression(AbstractExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def interpret(self, context):
        return self.left.interpret(context) + self.right.interpret(context)


class SubtractExpression(AbstractExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def interpret(self, context):
        return self.left.interpret(context) - self.right.interpret(context)


class MultiplyExpression(AbstractExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def interpret(self, context):
        return self.left.interpret(context) * self.right.interpret(context)


class DivideExpression(AbstractExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def interpret(self, context):
        divisor = self.right.interpret(context)
        if divisor == 0:
            raise ZeroDivisionError("Division by zero")
        return self.left.interpret(context) / divisor


class Parser:
    def parse(self, expression):
        pass


class ArithmeticParser(Parser):
    def parse(self, expression):
        expression = expression.replace(" ", "")
        stack = []
        operators = {'+': AddExpression, '-': SubtractExpression, '*': MultiplyExpression, '/': DivideExpression}

        tokens = re.findall(r'(\d+|\w+|[\+\-\*\/])', expression)
        for token in tokens:
            if token.isdigit():
                stack.append(Number(int(token)))
            elif token.isalpha():
                stack.append(Variable(token))
            elif token in operators:
                right = stack.pop()
                left = stack.pop()
                stack.append(operators[token](left, right))
        return stack.pop()


if __name__ == "__main__":
    context = Context()
    parser = ArithmeticParser()

    while True:
        expression = input("Enter an arithmetic expression (or type 'exit' to quit): ")
        if expression.lower() == 'exit':
            break

        try:
            parsed_expression = parser.parse(expression)
            result = parsed_expression.interpret(context)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
