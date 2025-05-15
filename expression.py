# start = expression , ? end of input ? ;
# expression = additive ;
# additive = multiplicative , { ("+" | "-") , multiplicative } ;
# multiplicative = power , { ("*" | "/" | "%" ) , power } ;   (* UPDATED *)
# power = primary , [ "^" , power ] ;                         (* NEW *)
# primary = ? integer ? | ? variable ? | "(" , expression , ")"

import re


class ParserError(Exception):

    def __init__(self, message):
        super().__init__(f'PARSER ERROR DETECTED:\n{message}')


class ExpressionParser:

    EOI = '? end of input ?'

    def __init__(self, source, environment):
        self._environment = environment
        self._tokens = iter(re.findall(r'[a-z]+|\d+|\S', source, re.I)
                            + [self.EOI])
        self.advance()

    def advance(self):
        try:
            self._current = next(self._tokens)
        except StopIteration:
            self._current = None

    def expect(self, expected_tokens):
        if self._current not in expected_tokens:
            token_found_str = f'"{self._current}"'
            expected_tokens_str = \
                ", ".join([f'"{token}"' for token in expected_tokens])
            message = (f'Found the token: {token_found_str}\n'
                       f'But was expecting one of: {expected_tokens_str}')
            raise ParserError(message)
        original_current = self._current
        self.advance()
        return original_current

    # The code from this point forward is the implementation of the
    # grammar we are defining.

    def start(self):
        result = self.expression()
        self.expect([self.EOI])
        return result

    def expression(self):
        return self.additive()

    def additive(self):
        result = self.multiplicative()
        while self._current in ['+', '-']:
            match self.expect(['+', '-']):
                case '+':
                    result += self.multiplicative()
                case '-':
                    result -= self.multiplicative()
        return result

    def multiplicative(self):
        result = self.power()
        while self._current in ['*', '/', '%']:
            match self.expect(['*', '/', '%']):
                case '*':
                    result *= self.power()
                case '/':
                    result //= self.power()
                case '%':
                    result %= self.power()
        return result

    def power(self):
        result = self.primary()
        if self._current == '^':
            self.advance()
            result **= self.power()
        return result

    def primary(self):
        current = self._current
        if current.isdigit():
            result = int(self._current)
            self.advance()
            return result
        if current.isalpha():
            if current not in self._environment:
                raise ParserError(
                    f'Variable "{current}" not found in '
                    f'environment {self._environment}')
            self.advance()
            return self._environment[current]
        if current == '(':
            self.advance()
            result = self.expression()
            self.expect([')'])
            return result
        token_found_str = f'"{current}"'
        message = (f'Found the token: {token_found_str}\n'
                   f'But was expecting an integer, variable or "("')
        raise ParserError(message)


if __name__ == '__main__':
    # expression = '11 * 2 / (15 - 10) + 20 % 3'
    expression = '11 * t + 2 ^ t ^ 2 - t + 1'
    environment = {'t': 3}
    evaluator = ExpressionParser(expression, environment)
    try:
        result = evaluator.start()
        print(f'{expression} = {result}')
    except ParserError as e:
        print(e)
