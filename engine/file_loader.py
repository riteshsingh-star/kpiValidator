import pandas as pd


class FileLoader:

    @staticmethod
    def load_file(file_path, parameter_name=None):

        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)

        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)

        elif file_path.endswith(".parquet"):
            df = pd.read_parquet(file_path)

        else:
            raise Exception(f"Unsupported file format: {file_path}")

        # Standardize columns
        if len(df.columns) >= 2:
            df = df.iloc[:, :2]

            if parameter_name:
                df.columns = ["Timestamp", parameter_name]

        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        return df