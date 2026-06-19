from interface.mapping_engine.column_mapper import ColumnMapper


class KPISpecEngine:

    @staticmethod
    def build_from_llm(llm_output, dataframe):

        # STEP 1: resolve variables to real columns
        mapped_variables = ColumnMapper.map_variables_to_columns(
            llm_output["variables"],
            dataframe
        )

        return {
            "kpi_name": llm_output["kpi_name"],
            "formula": llm_output["formula"],
            "variables": mapped_variables,
            "base_granularity": llm_output.get("base_granularity", "1Minute"),
            "generate_shifts": llm_output.get("generate_shifts", False),
            "parameters": []
        }