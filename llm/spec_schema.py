KPI_SPEC_SCHEMA = {
    "type": "object",
    "properties": {
        "kpi_name": {"type": "string"},
        "variables": {
            "type": "object",
            "additionalProperties": {"type": "string"}
        },
        "formula": {"type": "string"},
        "base_granularity": {"type": "string"},
        "generate_shifts": {"type": "boolean"}
    },
    "required": ["kpi_name", "variables", "formula"]
}