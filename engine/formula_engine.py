from engine.formula_function import (
    avg,
    first,
    last,
    max_value,
    min_value,
    sum_value
)


class FormulaEngine:

    @staticmethod
    def evaluate(formula, dataframe, variables=None):
        if variables is None:
            variables = {}

        
        # FUNCTION CONTEXT
        context = {
            "first": first,
            "last": last,
            "avg": avg,
            "sum": sum_value,
            "min": min_value,
            "max": max_value
        }

        
        # DATAFRAME COLUMNS
        for column in dataframe.columns:
            if column != "Timestamp":
                context[column] = dataframe[column]

        
        # VARIABLES
        context.update(variables)

        
        # MULTILINE FORMULA SUPPORT
        if isinstance(formula, list):
            last_expression = None

            for line in formula:
                line = line.strip()
                if not line:
                    continue

                if "=" in line and not line.startswith(("if", "for")):
                    variable_name, expression = line.split("=", 1)
                    variable_name = variable_name.strip()
                    expression = expression.strip()

                    value = eval(expression, {}, context)
                    context[variable_name] = value
                else:
                    last_expression = line

            if last_expression is None:
                raise Exception("No executable formula found.")

            return eval(last_expression, {}, context)

        
        # SINGLE LINE SUPPORT
        if formula is None:
            raise Exception("Formula cannot be None.")

        formula = str(formula).replace("\n", " ").strip()
        return eval(formula, {}, context)