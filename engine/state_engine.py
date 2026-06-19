import pandas as pd


class StateEngine:

    @staticmethod
    def evaluate(expression, df):

        expression = expression.strip()

        operators = [
            ">=",
            "<=",
            "==",
            "!=",
            ">",
            "<"
        ]

        for operator in operators:

            if operator in expression:

                parameter, threshold = (
                    expression.split(
                        operator,
                        1
                    )
                )

                parameter = parameter.strip()

                threshold = float(
                    threshold.strip()
                )

                series = df[
                    parameter
                ]

                if operator == ">":
                    return (
                        series > threshold
                    ).astype(int)

                if operator == "<":
                    return (
                        series < threshold
                    ).astype(int)

                if operator == ">=":
                    return (
                        series >= threshold
                    ).astype(int)

                if operator == "<=":
                    return (
                        series <= threshold
                    ).astype(int)

                if operator == "==":
                    return (
                        series == threshold
                    ).astype(int)

                if operator == "!=":
                    return (
                        series != threshold
                    ).astype(int)

        raise Exception(
            f"Invalid state expression: {expression}"
        )