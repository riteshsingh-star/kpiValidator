import sys

from engine.comparison_engine import ComparisonEngine
from engine.report_generator import ReportGenerator
from engine.summary_generator import SummaryGenerator


class KPIValidator:

    GRANULARITIES = [
        "1Min"
    ]

    @staticmethod
    def validate(kpi_name):

        for granularity in KPIValidator.GRANULARITIES:

            expected_file = (
                f"expected/{kpi_name}_{granularity}.csv"
            )

            actual_file = (
                f"actual/{kpi_name}_{granularity}.csv"
            )

            try:

                result = ComparisonEngine.compare(
                    expected_file,
                    actual_file
                )

                if result.empty:

                    print(
                        f"\nNo comparable rows "
                        f"for {granularity}"
                    )

                    continue

                pass_count = len(
                    result[
                        result["Status"] == "PASS"
                    ]
                )

                fail_count = len(
                    result[
                        result["Status"] == "FAIL"
                    ]
                )

                print(
                    f"\n{kpi_name} - {granularity}"
                )

                print("------------------")
                print("PASS :", pass_count)
                print("FAIL :", fail_count)

                # -----------------------------
                # Failed Records Summary
                # -----------------------------
                if fail_count > 0:

                    failed_rows = result[
                        result["Status"] == "FAIL"
                    ]

                    print("\nFailed Records")
                    print("-" * 120)

                    for _, row in (
                        failed_rows.head(20).iterrows()
                    ):

                        print(
                            f"Timestamp={row['Timestamp']} | "
                            f"Expected={row['Expected']:.6f} | "
                            f"Actual={row['Actual']:.6f} | "
                            f"Difference={row['Difference']:.6f} | "
                            f"Difference%={row['DifferencePercent']:.4f}"
                        )

                    if len(failed_rows) > 50:

                        print(
                            f"\nShowing first 20 failures "
                            f"out of {len(failed_rows)} "
                            f"total failures."
                        )

                    fail_file = (
                        f"reports/"
                        f"{kpi_name}_{granularity}_FailedRows.csv"
                    )

                    failed_rows.to_csv(
                        fail_file,
                        index=False
                    )

                    print(
                        f"\nFailure report generated: "
                        f"{fail_file}"
                    )

                # -----------------------------
                # Detailed Validation Report
                # -----------------------------
                ReportGenerator.save_validation_report(
                    result,
                    f"{kpi_name}_{granularity}_Validation"
                )

                summary = SummaryGenerator.generate(
                    result
                )

                print("\nSummary")
                print("-------")

                for key, value in summary.items():

                    print(
                        f"{key}: {value}"
                    )

            except Exception as e:

                print(
                    f"\nSkipped "
                    f"{granularity}: {e}"
                )


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Usage: python KPIValidator.py <KPI_NAME>"
        )

        sys.exit(1)

    kpi_name = sys.argv[1]

    KPIValidator.validate(
        kpi_name
    )