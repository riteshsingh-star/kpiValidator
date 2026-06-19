from engine.granularity_manager import GranularityManager


class ConfigValidator:

    @staticmethod
    def validate(config):

        errors = []

        
        # 1. Required fields
        required_fields = [
            "kpi_name",
            "formula",
            "parameters"
        ]

        for field in required_fields:

            if field not in config:
                errors.append(
                    f"Missing required field: {field}"
                )

        
        # 2. Validate parameters
        if "parameters" in config:

            for p in config["parameters"]:

                if "name" not in p:
                    errors.append("Parameter missing 'name'")

                if "file" not in p:
                    errors.append("Parameter missing 'file'")

        
        # 3. Validate granularity
        if "base_granularity" in config:

            bg = config["base_granularity"]

            if bg not in GranularityManager.GRANULARITIES:

                errors.append(
                    f"Invalid base_granularity: {bg}. "
                    f"Valid: {list(GranularityManager.GRANULARITIES.keys())}"
                )

        
        # 4. Validate shifts
        if config.get("generate_shifts", False):

            valid_shifts = {"Shift1", "Shift2", "Shift3"}

            # nothing strict yet, but hook for future
            config_shifts = config.get("shifts", valid_shifts)

            if not isinstance(config_shifts, (list, set)):

                errors.append(
                    "Shifts must be list or set"
                )

        
        # Result
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }