# KPIValidator

KPIValidator is a robust engine designed to calculate, analyze, and validate Key Performance Indicators (KPIs) from raw time-series data. It supports multi-granularity windowing, complex formula evaluation, and automated "Expected vs Actual" validation.

## 🚀 Features

- **Multi-Granularity Engine**: Automatically calculates KPIs across various time windows (1Min, 5Min, 15Min, 1Hr, etc.).
- **Formula Engine**: Supports custom formulas using functions like `first()`, `last()`, `avg()`, and `sum()`.
- **Automated Validation**: Compare calculated results against "ground truth" data with detailed deviation analysis.
- **Dual Reporting**: Generates both CSV and JSON reports for easy integration with Excel or Dashboards.
- **Shift Management**: Supports KPI calculation based on production shifts.
- **LLM Integration**: Experimental support for Natural Language to KPI specification using RAG.

## 🛠️ Installation

1. Ensure you have Python 3.8+ installed.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## 📖 Usage

### 1. Running a KPI Calculation
To execute a KPI calculation based on a configuration file in the `config/` directory:

```bash
python app.py <config_name>
```
*Example:* `python app.py Test_Production`

### 2. Running Validation
To compare `expected` vs `actual` results and generate a validation report:

```bash
python KPIValidator.py
```

## 📂 Project Structure

- `app.py`: Main entry point for KPI execution.
- `KPIValidator.py`: Script for result validation and comparison.
- `engine/`: Core logic for formulas, windows, and reporting.
- `config/`: JSON files defining KPI formulas and data sources.
- `data/`: Raw input CSV files.
- `actual/` / `expected/`: Data used for validation comparisons.
- `output/`: Detailed results for each granularity.
- `reports/`: Aggregated execution and validation reports.

## ⚙️ Configuration Example

KPIs are defined in JSON:
```json
{
    "kpi_name": "Test_Production",
    "formula": "(last(Ndk_Produced)-first(Ndk_Produced)) + (last(Odk_Produced)-first(Odk_Produced))",
    "parameters": [
        { "name": "Ndk_Produced", "file": "data/Ndk_Produced.csv" },
        { "name": "Odk_Produced", "file": "data/Odk_Produced.csv" }
    ]
}
```

---
*Developed for KPI Validation and Analysis.*
