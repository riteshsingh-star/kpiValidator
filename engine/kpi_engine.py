import json
from pathlib import Path
import pandas as pd

from engine.config_validator import ConfigValidator
from engine.file_loader import FileLoader
from engine.formula_preprocesser import FormulaPreprocessor
from engine.formula_validator import FormulaValidator
from engine.granularity_manager import GranularityManager
from engine.parameter_manager import ParameterManager
from engine.shift_manager import ShiftManager
from engine.window_engine import WindowEngine


class KPIEngine:

    @staticmethod
    def run(config):

        granularity_results = {}
        shift_results = {}

      
        # CONFIG VALIDATION
        validation_result = ConfigValidator.validate(config)

        if not validation_result["valid"]:
            print("\nCONFIG VALIDATION FAILED")
            print("------------------------")

            for err in validation_result["errors"]:
                print(f"ERROR: {err}")

            raise Exception("Invalid KPI configuration")

      
        # OUTPUT DIRECTORIES
        Path("output").mkdir(exist_ok=True)
        Path("reports").mkdir(exist_ok=True)

      
        # LOAD PARAMETER FILES
        parameter_dfs = []

        for parameter in config["parameters"]:
            df = FileLoader.load_file(parameter["file"], parameter["name"])
            parameter_dfs.append(df)

      
        # MERGE PARAMETERS
        if len(parameter_dfs) == 0:
            if "start_time" not in config or "end_time" not in config:
                raise Exception(
                    "Time-based KPI requires start_time and end_time."
                )

            start_time = pd.to_datetime(config["start_time"])
            end_time = pd.to_datetime(config["end_time"])

            merged = pd.DataFrame({
                "Timestamp": pd.date_range(
                    start=start_time, end=end_time, freq="1min"
                )
            })
        else:
            # Ensure requested boundaries are included in the merge base
            if "start_time" in config and "end_time" in config:
                boundary_df = pd.DataFrame({
                    "Timestamp": [
                        pd.to_datetime(config["start_time"]),
                        pd.to_datetime(config["end_time"])
                    ]
                })
                parameter_dfs.append(boundary_df)

            merged = ParameterManager.merge(parameter_dfs)

      
        # APPLY KPI TIME WINDOW
        merged["Timestamp"] = pd.to_datetime(merged["Timestamp"])

        if "start_time" in config:
            start_time = pd.to_datetime(config["start_time"])
            merged = merged[merged["Timestamp"] >= start_time]

        if "end_time" in config:
            end_time = pd.to_datetime(config["end_time"])
            merged = merged[merged["Timestamp"] <= end_time]

      
        # FORMULA
        raw_formula = config["formula"]
        formula = FormulaPreprocessor.normalize(raw_formula)

      
        # FORMULA VALIDATION
        validation = FormulaValidator.validate(
            formula, config["parameters"], config.get("variables", {})
        )

        if not validation["valid"]:
            print("\nFormula Validation Failed")
            print("Missing Parameters:", validation["missing"])
            raise Exception("Formula validation failed.")

        print("\nFormula Validation")
        print("-------------------")
        print("Required :", validation["required"])
        print("Configured :", validation["configured"])
        print("Validation Passed")

      
        # FORMAT GRANULARITY NAME
        def format_granularity_name(name):
            if "Minutes" in name:
                return name.replace("Minutes", "Min")
            if "Minute" in name:
                return name.replace("Minute", "Min")
            return name

      
        # REGULAR GRANULARITIES
        for granularity_name, frequency in GranularityManager.GRANULARITIES.items():
            result = WindowEngine.calculate(
                merged,
                formula,
                frequency,
                config.get("variables", {}),
                kpi_name=config["kpi_name"],
                end_time=config.get("end_time"),
            )

            granularity_results[granularity_name] = result

            file_name = (
                f"output/"
                f"{config['kpi_name']}_"
                f"{format_granularity_name(granularity_name)}.csv"
            )

            result.to_csv(file_name, index=False)
            print(f"Generated: {file_name}")

      
        # SHIFT EXECUTION
        if config.get("generate_shifts", False):
            base_granularity = config.get("base_granularity", "1Minute")

            aliases = {
                "1Minutes": "1Minute",
                "5Minute": "5Minutes",
                "10Minute": "10Minutes",
                "15Minute": "15Minutes",
                "20Minute": "20Minutes",
                "30Minute": "30Minutes",
                "2Hour": "2Hours",
                "6Hour": "6Hours",
                "8Hour": "8Hours",
                "12Hour": "12Hours",
            }

            base_granularity = aliases.get(base_granularity, base_granularity)

            if base_granularity not in GranularityManager.GRANULARITIES:
                raise Exception(f"Invalid base_granularity: {base_granularity}")

            frequency = GranularityManager.GRANULARITIES[base_granularity]

            shifts = {
                "Shift1": ShiftManager.get_shift1(merged),
                "Shift2": ShiftManager.get_shift2(merged),
                "Shift3": ShiftManager.get_shift3(merged),
            }

            for shift_name, shift_df in shifts.items():
                result = WindowEngine.calculate(
                    shift_df,
                    formula,
                    frequency,
                    config.get("variables", {}),
                    kpi_name=config["kpi_name"],
                )

                shift_results[shift_name] = result

                file_name = f"output/{config['kpi_name']}_{shift_name}.csv"
                result.to_csv(file_name, index=False)
                print(f"Generated: {file_name}")

      
        # EXECUTION REPORT
        from engine.report_engine import ReportEngine

        report_df = ReportEngine.generate(
            config["kpi_name"], granularity_results, shift_results
        )

        report_csv = f"reports/{config['kpi_name']}_execution_report.csv"
        report_json = f"reports/{config['kpi_name']}_execution_report.json"

        report_df.to_csv(report_csv, index=False)

        with open(report_json, "w") as f:
            json.dump(report_df.to_dict(orient="records"), f, indent=4)

        print("\nExecution Completed")
        print("-------------------")
        print(f"KPI: {config['kpi_name']}")
        print("Output Folder : output/")
        print("Report Folder : reports/")

        return {
            "kpi_name": config["kpi_name"],
            "granularity_results": granularity_results,
            "shift_results": shift_results,
            "report_csv": report_csv,
            "report_json": report_json,
        }