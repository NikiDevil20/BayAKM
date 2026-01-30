from typing import Union

from sympy.physics.units import length


class SumFormulaConverter:
    def __init__(self):
        pass

    @staticmethod
    def make_formula(formula: str):
        if not isinstance(formula, str):
            return formula

        sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        supers_map = {"t": "ᵗ", "i": "ᶦ"}
        out = ""
        numeric = 0
        alphabet = 0
        exclude = "G"
        _length = len(formula)

        for index, character in enumerate(formula):
            if index >=1 and character.isdigit() and formula[index-1] == exclude:
                out += character
                numeric += 1
                continue

            if character in supers_map and (index + 2) < _length:
                next_chars = formula[index+1] + formula[index+2]
                if ((character == "t" and next_chars == "Bu")
                        or (character == "i" and next_chars == "Pr")):
                    out += supers_map[character]
                    alphabet += 1
                    continue

            out += character.translate(sub)
            if character.isdigit():
                numeric += 1
            else:
                alphabet += 1
        if numeric > alphabet:
            return formula

        return out

    @staticmethod
    def make_string(formula: str):
        if not isinstance(formula, str):
            return formula
        normal = str.maketrans("₀₁₂₃₄₅₆₇₈₉ᵗᶦ", "0123456789ti")
        return formula.translate(normal)