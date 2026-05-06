import json
import os


class Region:

    def __init__(self, data):

        self.id = data["id"]
        self.name = data["name"]

        self.biome = data.get("biome", "unknown")
        self.danger_level = data.get("danger_level", 1)

        self.culture = data.get("culture", "neutral")

        self.controlling_faction = data.get(
            "controlling_faction"
        )

        self.weather = data.get("weather", "clear")

        self.corruption = data.get("corruption", 0)

        self.stability = data.get("stability", 100)

        self.resources = data.get("resources", {})

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "biome": self.biome,
            "danger_level": self.danger_level,
            "culture": self.culture,
            "controlling_faction": self.controlling_faction,
            "weather": self.weather,
            "corruption": self.corruption,
            "stability": self.stability,
            "resources": self.resources
        }


class RegionSystem:

    def __init__(self, path="data/regions.json"):

        self.path = path
        self.regions = {}

        self.load_regions()

    def load_regions(self):

        if not os.path.exists(self.path):

            print(
                f"[RegionSystem] "
                f"File non trovato: {self.path}"
            )

            return

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        self.regions.clear()

        for region_data in data:

            region = Region(region_data)

            self.regions[region.id] = region

        print(
            f"[RegionSystem] "
            f"Caricate {len(self.regions)} regioni."
        )

    def get_region(self, region_id):

        return self.regions.get(region_id)

    def all_regions(self):

        return list(self.regions.values())

    def save_regions(self):

        data = []

        for region in self.regions.values():

            data.append(region.to_dict())

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print("[REGIONS] Salvate.")