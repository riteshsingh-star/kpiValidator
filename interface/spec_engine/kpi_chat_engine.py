from llm.kpi_llm_client import KPI_LLM_Client
from interface.spec_engine.kpi_spec_engine import KPISpecEngine
from engine.kpi_engine import KPIEngine
from kpi_knowledge.kpi_index import KPIIndex
from kpi_knowledge.kpi_memory import KPIMemory
from engine.comparison_engine import ComparisonEngine


class KPIChatEngine:

    @staticmethod
    def ask(query: str, expected_file=None, actual_file=None):

        print("\nQUERY:", query)

        # -----------------------------
        # STEP 1: RAG SEARCH
        # -----------------------------
        index = KPIIndex()
        rag_result = index.search(query)

        if rag_result["found"]:
            llm_output = {
                "kpi_name": rag_result["kpi"]["kpi_name"],
                "formula": rag_result["kpi"]["formula"],
                "variables": rag_result["kpi"]["variables"],
                "base_granularity": "1Minute",
                "generate_shifts": True
            }
        else:
            llm_output = KPI_LLM_Client.parse(query)

        # -----------------------------
        # STEP 2: BUILD CONFIG
        # -----------------------------
        df = None  # plug loader in real system

        config = KPISpecEngine.build_from_llm(llm_output, df)

        # -----------------------------
        # STEP 3: EXECUTE KPI
        # -----------------------------
        KPIEngine.run(config)

        # -----------------------------
        # STEP 4: VALIDATION (FEEDBACK LOOP)
        # -----------------------------
        if expected_file and actual_file:

            comparison = ComparisonEngine.compare(
                expected_file,
                actual_file
            )

            pass_count = len(comparison[comparison["Status"] == "PASS"])
            fail_count = len(comparison[comparison["Status"] == "FAIL"])

            deviation = comparison["DifferencePercent"].abs().max()

            status = "PASS" if fail_count == 0 else "FAIL"

            print("\nFEEDBACK RESULT")
            print("----------------")
            print("PASS:", pass_count)
            print("FAIL:", fail_count)
            print("MAX DEVIATION:", deviation)

            # -----------------------------
            # STEP 5: LEARN
            # -----------------------------
            memory = KPIMemory()

            memory.update_feedback(
                config["kpi_name"],
                status,
                deviation
            )

            # If new KPI → store it
            if not rag_result["found"]:
                memory.save_kpi(config)