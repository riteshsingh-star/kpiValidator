import pandas as pd


class GranularityEngine:

    GRANULARITIES = {
        "1Minute": "1min",
        "5Minutes": "5min",
        "10Minutes": "10min",
        "15Minutes": "15min",
        "20Minutes": "20min",
        "30Minutes": "30min",
        "1Hour": "1h",
        "2Hours": "2h",
        "6Hours": "6h",
        "8Hours": "8h",
        "12Hours": "12h"
    }

    @staticmethod
    def generate(df, aggregation="mean"):

        results = {}

        df = df.copy()
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df = df.set_index("Timestamp")

        for name, freq in GranularityEngine.GRANULARITIES.items():

            if aggregation == "mean":
                resampled = df.resample(freq).mean()

            elif aggregation == "sum":
                resampled = df.resample(freq).sum()

            elif aggregation == "min":
                resampled = df.resample(freq).min()

            elif aggregation == "max":
                resampled = df.resample(freq).max()

            else:
                raise Exception(
                    f"Unsupported aggregation: {aggregation}"
                )

            results[name] = resampled.reset_index()

        return results