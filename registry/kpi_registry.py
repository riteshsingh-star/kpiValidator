class KPIRegistry:

    KPIS = {
        "Accessibility": {
            "formula": "SUM(success_attempts) / SUM(total_attempts) * 100",
            "parameters": [
                {
                    "name": "success_attempts",
                    "file": "data/success_attempts.csv"
                },
                {
                    "name": "total_attempts",
                    "file": "data/total_attempts.csv"
                }
            ]
        },

        "Availability": {
            "formula": "avg(uptime) * 100",
            "parameters": [
                {
                    "name": "uptime",
                    "file": "data/uptime.csv"
                }
            ]
        },

        "Traffic": {
            "formula": "sum(traffic_volume)",
            "parameters": [
                {
                    "name": "traffic_volume",
                    "file": "data/traffic.csv"
                }
            ]
        }
    }

    @staticmethod
    def get(kpi_name: str):

        return KPIRegistry.KPIS.get(kpi_name)