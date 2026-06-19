from pathlib import Path


class ReportGenerator:

    @staticmethod
    def save_validation_report(
        dataframe,
        report_name
    ):

        Path("reports").mkdir(
            exist_ok=True
        )

        file_path = (
            f"reports/{report_name}.csv"
        )

        dataframe.to_csv(
            file_path,
            index=False
        )

        print(
            f"\nReport Generated: {file_path}"
        )

        return file_path