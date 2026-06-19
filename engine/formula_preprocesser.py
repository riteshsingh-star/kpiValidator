import re


class FormulaPreprocessor:

    @staticmethod
    def normalize(formula: str) -> str:

        # Remove comments (# style)
        formula = re.sub(r"#.*", "", formula)

        # Split lines
        lines = formula.split("\n")

        cleaned_lines = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            cleaned_lines.append(line)

        return cleaned_lines