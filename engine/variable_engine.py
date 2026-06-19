from engine.formula_engine import FormulaEngine
from engine.state_engine import StateEngine


class VariableEngine:

    @staticmethod
    def evaluate(
        variables,
        dataframe
    ):

        context = {}

        for (
            variable_name,
            expression
        ) in variables.items():

            expression = (
                expression.strip()
            )

            # -----------------------------
            # STATE FUNCTION
            # Example:
            # a = state(TEST_RAW_PURE > 20)
            # -----------------------------
            if (
                expression.startswith(
                    "state("
                )
                and
                expression.endswith(
                    ")"
                )
            ):

                state_expression = (
                    expression[
                        len("state("):-1
                    ]
                )

                value = (
                    StateEngine.evaluate(
                        state_expression,
                        dataframe
                    )
                )

            # -----------------------------
            # NORMAL FORMULA
            # -----------------------------
            else:

                value = (
                    FormulaEngine.evaluate(
                        expression,
                        dataframe,
                        context
                    )
                )

            context[
                variable_name
            ] = value

        return context