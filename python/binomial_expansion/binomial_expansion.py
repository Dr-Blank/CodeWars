"""Binomial Expression using object oriented programming"""

import re
from typing import Any, Dict, Iterable


def expand(expr: str):
    pattern = re.compile(
        r"""\( # a literal (
            (-?\d*) # followed by the coefficient (+-)
            (\w*) # followed by the variable
            (\+?-?\d*) # followed by the constant
            \) # followed by a literal )
            \^ # followed by a literal ^
            (\d*) # followed by the power
            """,
        re.VERBOSE,
    )

    coefficient, variable, constant, power = re.findall(pattern, expr)[0]

    coefficient = -1 if coefficient == "-" else int(coefficient) if coefficient else 1
    variable = str(variable)
    power = int(power) if power else 1
    constant = int(constant) if constant else 0

    if power == 0:
        return "1"

    terms: Iterable[Term] = []
    for i, binomial_coefficient in enumerate(get_pascal_triangle(power)):
        term_coefficient: int = (
            binomial_coefficient * (coefficient**i) * (constant ** (power - i))
        )
        terms.append(Term(term_coefficient, variable, i))

    return str(Expression(terms))


def get_pascal_triangle(n: int):
    """returns the nth line of Pascal triangle, implements Dynamic programming"""
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]
    row = [1, 1]
    for _ in range(1, n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row


class Term:
    """ax^n is a term"""

    def __init__(self, coefficient: int, variable: Any = None, power: Any = None):
        if not variable:
            self.coefficient = coefficient
            self.variable = variable
            self.power = 0
            return

        if power is None:
            power = 1

        self.coefficient = coefficient
        self.variable = variable
        self.power = int(power)

    def __str__(self):
        if self.coefficient == 0:
            return ""

        return "{}{}".format(
            self._get_coefficient_str(),
            self.get_variable_str(),
        )

    def _get_coefficient_str(self):
        if self.coefficient == -1:
            if not self.variable or self.power == 0:
                return "-1"
            return "-"

        if self.coefficient == 1:
            if not self.power:
                return "1"
            return ""

        return f"{self.coefficient}"

    def get_variable_str(self):
        if not self.power:
            return ""

        if self.power == 1:
            return f"{self.variable}"

        return "{variable}^{power}".format(**self.__dict__)


class Expression:
    """A sum of terms is an expression"""

    def __init__(self, terms: Iterable[Term]):
        self.terms = list(terms)

    def __str__(self):
        self.simplify()
        if not self.terms:
            return "0"

        return "+".join(str(term) for term in self.terms).replace("+-", "-")

    def simplify(self):
        seen: Dict[str, int] = {}

        for term in self.terms:
            var = term.get_variable_str()
            # can not use an object as string, hence the variable power, which is unique, is used.
            # variable and power combo should be unique
            if var in seen:
                seen[var] += term.coefficient
            else:
                seen[var] = term.coefficient

        new_terms = sorted(
            (
                Term(coefficient, *var.split("^"))
                for var, coefficient in seen.items()
                if coefficient != 0
            ),
            key=lambda t: t.power,
            reverse=True,
        )
        self.terms = new_terms
