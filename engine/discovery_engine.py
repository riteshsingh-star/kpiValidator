import os
import pandas as pd
import glob


class DiscoveryEngine:

    @staticmethod
    def discover_parameters(directory: str):
        """
        Scans a directory for CSV/XLSX files and returns a map of {column_name: file_path}
        """
        catalog = {}
        
        # Support CSV, XLSX, Parquet
        extensions = ['**/*.csv', '**/*.xlsx', '**/*.parquet']
        files = []
        for ext in extensions:
            files.extend(glob.glob(os.path.join(directory, ext), recursive=True))

        for file_path in files:
            try:
                # We only need headers to catalog columns
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, nrows=0)
                elif file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path, nrows=0)
                elif file_path.endswith('.parquet'):
                    df = pd.read_parquet(file_path)
                
                # Assume first column is Timestamp, others are parameters
                cols = df.columns.tolist()
                for col in cols:
                    if col.lower() != 'timestamp':
                        # If duplicate columns across files, we take the first one found or handle it
                        if col not in catalog:
                            catalog[col] = file_path
            except Exception as e:
                print(f"Warning: Could not process {file_path} during discovery: {e}")

        return catalog
