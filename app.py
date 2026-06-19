from engine.config_loader import ConfigLoader
from engine.kpi_engine import KPIEngine
import sys

kpi_name = sys.argv[1]

config = ConfigLoader.load(f"config/{kpi_name}.json")

KPIEngine.run(config)