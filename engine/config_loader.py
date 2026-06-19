import json


class ConfigLoader:

    @staticmethod
    def load(config_file):

        with open(config_file, "r") as f:
            return json.load(f)