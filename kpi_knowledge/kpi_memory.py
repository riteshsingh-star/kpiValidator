import json
from datetime import datetime


class KPIMemory:

    def __init__(self, store_path="kpi_knowledge/kpi_store.json"):
        self.store_path = store_path

        with open(store_path, "r") as f:
            self.kpis = json.load(f)

    # -----------------------------
    # Save new KPI into memory
    # -----------------------------
    def save_kpi(self, kpi_spec: dict):

        self.kpis.append({
            "kpi_name": kpi_spec["kpi_name"],
            "formula": kpi_spec["formula"],
            "variables": kpi_spec["variables"],
            "created_at": str(datetime.now())
        })

        self._persist()

    # -----------------------------
    # Update KPI based on feedback
    # -----------------------------
    def update_feedback(self, kpi_name: str, status: str, deviation: float):

        for kpi in self.kpis:

            if kpi["kpi_name"] == kpi_name:

                if "history" not in kpi:
                    kpi["history"] = []

                kpi["history"].append({
                    "status": status,
                    "deviation": deviation,
                    "timestamp": str(datetime.now())
                })

        self._persist()

    # -----------------------------
    # Persist to disk
    # -----------------------------
    def _persist(self):

        with open(self.store_path, "w") as f:
            json.dump(self.kpis, f, indent=4)