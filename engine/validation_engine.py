from engine.comparison_engine import ComparisonEngine
from engine.report_generator import ReportGenerator
from engine.summary_generator import SummaryGenerator


class ValidationRunner:

    @staticmethod
    def run(kpi_name):

        granularities = [
            "1Min",
            "5Min",
            "10Min",
            "15Min",
            "20Min",
            "30Min",
            "1Hour",
            "2Hours",
            "6Hours",
            "8Hours",
            "12Hours",
            "Shift1",
            "Shift2",
            "Shift3"
        ]

        for granularity in granularities:

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

                ReportGenerator.save_validation_report(
                    result,
                    f"{kpi_name}_{granularity}_Validation"
                )

                summary = SummaryGenerator.generate(
                    result
                )

                print(
                    f"\n{kpi_name} - {granularity}"
                )
                print(summary)

            except Exception as e:

                print(
                    f"Validation skipped for "
                    f"{granularity}: {e}"
                )