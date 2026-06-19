import pandas as pd


class ShiftManager:

    @staticmethod
    def get_shift1(df):

        shift_df = df.copy()

        shift_df["Timestamp"] = pd.to_datetime(
            shift_df["Timestamp"]
        )

        return shift_df[
            (
                shift_df["Timestamp"].dt.time
                >= pd.Timestamp("10:00:00").time()
            )
            &
            (
                shift_df["Timestamp"].dt.time
                <= pd.Timestamp("14:00:00").time()
            )
        ]

    @staticmethod
    def get_shift2(df):

        shift_df = df.copy()

        shift_df["Timestamp"] = pd.to_datetime(
            shift_df["Timestamp"]
        )

        return shift_df[
            (
                shift_df["Timestamp"].dt.time
                > pd.Timestamp("14:00:00").time()
            )
            &
            (
                shift_df["Timestamp"].dt.time
                <= pd.Timestamp("22:00:00").time()
            )
        ]

    @staticmethod
    def get_shift3(df):

        shift_df = df.copy()

        shift_df["Timestamp"] = pd.to_datetime(
            shift_df["Timestamp"]
        )

        return shift_df[
            (
                shift_df["Timestamp"].dt.time
                > pd.Timestamp("22:00:00").time()
            )
            |
            (
                shift_df["Timestamp"].dt.time
                <= pd.Timestamp("06:00:00").time()
            )
        ]