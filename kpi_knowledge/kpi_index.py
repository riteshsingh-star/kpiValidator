import json
import difflib


class KPIIndex:

    def __init__(self, store_path="kpi_knowledge/kpi_store.json"):

        with open(store_path, "r") as f:
            self.kpis = json.load(f)

    def search(self, query: str):

        query = query.lower()

        names = [k["kpi_name"].lower() for k in self.kpis]

        # fuzzy match KPI names
        matches = difflib.get_close_matches(query, names, n=1, cutoff=0.4)

        if matches:
            for kpi in self.kpis:
                if kpi["kpi_name"].lower() == matches[0]:
                    return {
                        "found": True,
                        "kpi": kpi
                    }

        return {
            "found": False,
            "kpi": None
        }