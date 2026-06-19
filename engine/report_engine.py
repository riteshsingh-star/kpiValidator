import pandas as pd


class ReportEngine:

    @staticmethod
    def generate(kpi_name, granularity_results, shift_results):

        report_rows = []

        # -----------------------------
        # GRANULARITY REPORT
        # -----------------------------
        for g_name, df in granularity_results.items():

            if df.empty:
                continue

            report_rows.append({
                "Type": "Granularity",
                "Name": g_name,
                "TotalRows": len(df),
                "MaxKPI": df[kpi_name].max(),
                "MinKPI": df[kpi_name].min(),
                "AvgKPI": df[kpi_name].mean()
            })

        # -----------------------------
        # SHIFT REPORT
        # -----------------------------
        for s_name, df in shift_results.items():

            if df.empty:
                continue

            report_rows.append({
                "Type": "Shift",
                "Name": s_name,
                "TotalRows": len(df),
                "MaxKPI": df[kpi_name].max(),
                "MinKPI": df[kpi_name].min(),
                "AvgKPI": df[kpi_name].mean()
            })

        report_df = pd.DataFrame(report_rows)

        return report_df