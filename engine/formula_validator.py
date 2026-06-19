import re

class FormulaValidator:

    FUNCTIONS = {
        "first",
        "last",
        "avg",
        "sum",
        "min",
        "max",
        "state",
        "window_duration",
        "window_start",
        "window_end"
    }


    # EXTRACT LOCAL VARIABLES
    @staticmethod
    def extract_local_variables(formula):

        local_variables = []

        if not isinstance(formula, list):
            return local_variables

        for line in formula:

            line = str(line).strip()

            if (
                "=" in line
                and not line.startswith(
                    ("if", "for")
                )
            ):

                variable_name = (
                    line.split("=")[0]
                    .strip()
                )

                local_variables.append(
                    variable_name
                )

        return local_variables


    # PARAMETER EXTRACTION
    @staticmethod
    def extract_parameters(
        formula,
        variable_names=None
    ):

        if formula is None:
            return []

        if isinstance(formula, list):
            formula = " ".join(
                map(str, formula)
            )

        if isinstance(formula, dict):
            formula = str(formula)

        if variable_names is None:
            variable_names = []

        tokens = re.findall(
            r"[A-Za-z_][A-Za-z0-9_]*",
            str(formula)
        )

        parameters = []

        for token in tokens:

            if token in FormulaValidator.FUNCTIONS:
                continue

            if token in variable_names:
                continue

            parameters.append(
                token
            )

        return sorted(
            list(
                set(parameters)
            )
        )


    # VALIDATE VARIABLE EXPRESSIONS
    @staticmethod
    def validate_variables(
        variables,
        configured_parameters
    ):

        if not variables:
            return []

        configured_names = [
            p["name"]
            for p in configured_parameters
        ]

        variable_names = list(
            variables.keys()
        )

        missing = []

        for _, expression in variables.items():

            required = (
                FormulaValidator.extract_parameters(
                    expression,
                    variable_names
                )
            )

            for parameter in required:

                if parameter not in configured_names:

                    missing.append(
                        parameter
                    )

        return list(
            set(missing)
        )


    # MAIN VALIDATION
    @staticmethod
    def validate(
        formula,
        configured_parameters,
        variables=None
    ):

        if formula is None:
            formula = ""

        variable_names = []

        # Variables from config
        if variables:
            variable_names.extend(
                variables.keys()
            )

        # Variables declared inside formula
        local_variables = (
            FormulaValidator.extract_local_variables(
                formula
            )
        )

        variable_names.extend(
            local_variables
        )

        variable_names = list(
            set(variable_names)
        )

        required_parameters = (
            FormulaValidator.extract_parameters(
                formula,
                variable_names
            )
        )

        configured_names = [
            p["name"]
            for p in configured_parameters
        ]

        missing_parameters = []

        for parameter in required_parameters:

            if parameter not in configured_names:

                missing_parameters.append(
                    parameter
                )

        variable_missing = (
            FormulaValidator.validate_variables(
                variables,
                configured_parameters
            )
        )

        missing_parameters.extend(
            variable_missing
        )

        missing_parameters = list(
            set(missing_parameters)
        )

        return {
            "required": required_parameters,
            "configured": configured_names,
            "variables": variable_names,
            "missing": missing_parameters,
            "valid": len(
                missing_parameters
            ) == 0
        }
