import pandas as pd


class ComparisonEngine:

    @staticmethod
    def compare(
        expected_file,
        actual_file,
        tolerance=0.2
    ):

        expected = pd.read_csv(
            expected_file
        )

        actual = pd.read_csv(
            actual_file
        )


        # Detect KPI Column
        def get_kpi_col(df):

            cols = [
                c
                for c in df.columns
                if c != "Timestamp"
            ]

            if not cols:

                raise Exception(
                    "No KPI column found."
                )

            return cols[0]

        expected_kpi = get_kpi_col(
            expected
        )

        actual_kpi = get_kpi_col(
            actual
        )

        # Standardize KPI Columns
        expected = expected.rename(
            columns={
                expected_kpi: "Expected"
            }
        )

        actual = actual.rename(
            columns={
                actual_kpi: "Actual"
            }
        )


        # Merge
        merged = expected.merge(
            actual,
            on="Timestamp",
            how="inner"
        )

        print(
            f"\nExpected rows: "
            f"{len(expected)}"
        )

        print(
            f"Actual rows: "
            f"{len(actual)}"
        )

        print(
            f"Merged rows: "
            f"{len(merged)}"
        )

        if merged.empty:

            raise Exception(
                "No matching timestamps found "
                "between expected and actual files."
            )

        results = []


        # Compare Rows
        for _, row in merged.iterrows():

            expected_value = row[
                "Expected"
            ]

            actual_value = row[
                "Actual"
            ]

            difference = round(
                actual_value - expected_value, 10
            )

            if expected_value != 0:

                difference_percent = round(
                    (difference / expected_value) * 100, 6
                )

            else:

                difference_percent = 0

            status = (
                "PASS"
                if abs(
                    difference_percent
                ) <= tolerance
                else "FAIL"
            )

            results.append(
                {
                    "Timestamp":
                        row["Timestamp"],

                    "Expected":
                        expected_value,

                    "Actual":
                        actual_value,

                    "Difference":
                        difference,

                    "DifferencePercent":
                        difference_percent,

                    "Status":
                        status
                }
            )


        # Return Result
        return pd.DataFrame(
            results,
            columns=[
                "Timestamp",
                "Expected",
                "Actual",
                "Difference",
                "DifferencePercent",
                "Status"
            ]
        )