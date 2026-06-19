import pandas as pd

from engine.formula_engine import FormulaEngine
from engine.variable_engine import VariableEngine


class WindowEngine:

    @staticmethod
    def calculate(df, formula, frequency, variables=None, kpi_name="KPI", end_time=None):
        if variables is None:
            variables = {}

        df = df.copy()
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df = df.sort_values("Timestamp")
        df = df.set_index("Timestamp")

        # First timestamp becomes bucket origin
        origin_timestamp = df.index.min().replace(second=0, microsecond=0)

        # Last raw data timestamp
        if end_time:
            max_timestamp = pd.to_datetime(end_time)
        else:
            max_timestamp = df.index.max()

        results = []
        grouped = df.groupby(
            pd.Grouper(freq=frequency, origin=origin_timestamp)
        )

        for timestamp, group in grouped:
            if len(group) == 0:
                continue

            group = group.reset_index()

            try:
                variable_values = {}

                if variables:
                    variable_values = VariableEngine.evaluate(variables, group)


                # Window Context
                window_start = timestamp
                window_end = timestamp + pd.to_timedelta(frequency)
                window_duration = (window_end - window_start).total_seconds()

                variable_values.update({
                    "window_start": window_start,
                    "window_end": window_end,
                    "window_duration": window_duration,
                })

                value = FormulaEngine.evaluate(formula, group, variable_values)

                # Bucket end timestamp
                bucket_timestamp = timestamp + pd.to_timedelta(frequency)

                # Stop if the window START exceeds available data
                if timestamp > max_timestamp:
                    break

                results.append({"Timestamp": bucket_timestamp, kpi_name: value})

            except Exception as e:
                print(f"Error processing bucket {timestamp}: {e}")

        result_df = pd.DataFrame(results)

        # Match actual KPI format
        if not result_df.empty:
            result_df["Timestamp"] = (
                pd.to_datetime(result_df["Timestamp"]).dt.strftime(
                    "%m/%d/%Y %H:%M:%S"
                )
            )

        return result_df