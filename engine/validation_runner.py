from engine.formula_engine import FormulaEngine


class VariableEngine:

    @staticmethod
    def evaluate(
        variables,
        dataframe
    ):

        context = {}

        for variable_name, expression in variables.items():

            value = FormulaEngine.evaluate(
                expression,
                dataframe,
                context
            )

            context[variable_name] = value

            print(
                f"{variable_name} = {value}"
            )

        return context