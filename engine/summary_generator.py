class SummaryGenerator:

    @staticmethod
    def generate(result_df):

        total = len(result_df)

        pass_count = len(
            result_df[result_df["Status"] == "PASS"]
        )

        fail_count = len(
            result_df[result_df["Status"] == "FAIL"]
        )

        success_rate = (
            (pass_count / total) * 100
            if total > 0
            else 0
        )

        max_deviation = (
            result_df["DifferencePercent"]
            .abs()
            .max()
        )

        return {
            "TotalRows": total,
            "PASS": pass_count,
            "FAIL": fail_count,
            "SuccessRate": round(success_rate, 2),
            "MaxDeviationPercent": round(max_deviation, 4)
        }