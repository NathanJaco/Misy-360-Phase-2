import json
from pathlib import Path


class DataManager:
    def __init__(self, filepath):
        self.filepath = Path(filepath)

    def load_data(self):
        data = []

        if self.filepath.exists():
            with open(self.filepath, "r") as f:
                data = json.load(f)

        return data

    def save_data(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f)