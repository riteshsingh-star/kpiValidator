import sys
import os
import json
from llm.kpi_llm_client import KPI_LLM_Client
from engine.discovery_engine import DiscoveryEngine
from engine.kpi_engine import KPIEngine
import difflib

def auto_scale_kpi(prompt: str, data_dir: str = "data"):
    print(f"\n--- SCALING KPI: {prompt} ---")
    
    # STEP 1: Discover available columns and their files
    print(f"Discovering parameters in {data_dir}...")
    catalog = DiscoveryEngine.discover_parameters(data_dir)
    available_columns = list(catalog.keys())
    print(f"Available columns: {available_columns}")

    # STEP 2: Get KPI specification from LLM
    print("Asking LLM for KPI specification...")
    llm_output = KPI_LLM_Client.parse(prompt)
    print(f"LLM Output: {json.dumps(llm_output, indent=2)}")

    # STEP 3: Map variables to real files
    parameters = []
    variables_mapped = {}
    
    for var_name, col_suggestion in llm_output["variables"].items():
        # Fuzzy match the suggestion against available columns
        matches = difflib.get_close_matches(col_suggestion, available_columns, n=1, cutoff=0.3)
        if not matches:
            print(f"Error: Could not find a match for '{col_suggestion}' in data directory.")
            return

        real_col = matches[0]
        file_path = catalog[real_col]
        
        variables_mapped[var_name] = real_col
        parameters.append({
            "name": real_col,
            "file": file_path
        })
        print(f"Mapped variable '{var_name}' -> column '{real_col}' in file '{file_path}'")

    # STEP 4: Construct final config
    config = {
        "kpi_name": llm_output["kpi_name"],
        "formula": llm_output["formula"],
        "variables": variables_mapped, # Note: if formula uses business names, engine handles it if mapped correctly
        "base_granularity": llm_output.get("base_granularity", "1Minute"),
        "generate_shifts": llm_output.get("generate_shifts", False),
        "parameters": parameters
    }
    
    # If the LLM returned raw column names in formula but we mapped them to variables,
    # the engine usually expects the formula to use the variable names.
    # KPI_LLM_SYSTEM_PROMPT says: "Formula must use ONLY variable names, not raw column names"
    
    print("\nGenerated Config:")
    print(json.dumps(config, indent=2))

    # STEP 5: Run KPI Engine
    print("\nRunning KPI Engine...")
    KPIEngine.run(config)
    print("\n--- KPI EXECUTION COMPLETE ---")
    print(f"Expected files generated in 'output/' and 'reports/' folders.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_runner.py \"Your KPI Prompt\" [data_directory]")
        sys.exit(1)
    
    prompt = sys.argv[1]
    data_dir = sys.argv[2] if len(sys.argv) > 2 else "data"
    
    auto_scale_kpi(prompt, data_dir)
