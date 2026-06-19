import difflib


class ColumnMapper:

    @staticmethod
    def map_variables_to_columns(variables: dict, dataframe):

        columns = [col for col in dataframe.columns if col != "Timestamp"]

        resolved = {}

        for var_name, var_value in variables.items():

            # direct match
            if var_value in columns:
                resolved[var_name] = var_value
                continue

            # fuzzy match (IMPORTANT)
            match = difflib.get_close_matches(
                var_value,
                columns,
                n=1,
                cutoff=0.4
            )

            if match:
                resolved[var_name] = match[0]
            else:
                raise Exception(
                    f"Cannot map variable '{var_value}' to any column in data"
                )

        return resolved