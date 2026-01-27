

class SumFormulaConverter:
    def __init__(self):
        pass

    @staticmethod
    def subscript(formula: str):
        sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        out = ""
        numeric = 0
        alphabet = 0
        for character in formula:
            out += character.translate(sub)
            if character.isdigit():
                numeric += 1
            else:
                alphabet += 1
        if numeric > alphabet:
            return formula

        return out

    @staticmethod
    def plain(formula: str):
        normal = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
        out = ""
        for character in formula:
            out += character.translate(normal)

        return out