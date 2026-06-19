import pandas as pd


class ParameterManager:

    @staticmethod
    def merge(parameter_dfs):

        if not parameter_dfs:
            return pd.DataFrame()

        # Normalize timestamps and sort
        for i in range(len(parameter_dfs)):
            parameter_dfs[i]["Timestamp"] = pd.to_datetime(parameter_dfs[i]["Timestamp"])
            parameter_dfs[i] = parameter_dfs[i].sort_values("Timestamp")

        # Create a base dataframe with all unique timestamps from all parameters
        # to ensure no data is truncated because it's missing in the first file.
        all_timestamps = pd.concat([df[["Timestamp"]] for df in parameter_dfs])
        final_df = all_timestamps.drop_duplicates().sort_values("Timestamp")

        # Merge each parameter onto the master timeline
        for df in parameter_dfs:
            final_df = pd.merge_asof(
                final_df,
                df,
                on="Timestamp",
                direction="nearest",
                tolerance=pd.Timedelta("60s")
            )

        return final_df