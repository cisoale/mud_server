import random
import threading
import time

from core.simulation.global_events import event_bus


WEATHER_TYPES = [
    "clear",
    "rain",
    "fog",
    "storm"
]


class WorldTickSystem:

    def __init__(self, region_system):

        self.region_system = region_system
        self.running = False

    # =========================
    # START
    # =========================
    def start(self):

        if self.running:
            return

        self.running = True

        thread = threading.Thread(
            target=self.loop,
            daemon=True
        )

        thread.start()

        print("[WORLD TICK] Avviato")

    # =========================
    # LOOP
    # =========================
    def loop(self):

        print("[WORLD TICK] Loop attivo")

        while self.running:

            try:

                print("[WORLD TICK] Tick...")

                self.update_weather()

            except Exception as e:

                print(
                    f"[WORLD TICK ERROR] {e}"
                )

            # DEBUG
            time.sleep(10)

    # =========================
    # WEATHER UPDATE
    # =========================
    def update_weather(self):

        for region in self.region_system.all_regions():

            print(
                f"[DEBUG] Regione: "
                f"{region.name}"
            )

            old_weather = region.weather

            new_weather = random.choice(
                WEATHER_TYPES
            )

            region.weather = new_weather

            # =====================
            # WEATHER CHANGED
            # =====================
            if old_weather != new_weather:

                print(
                    f"[WEATHER] "
                    f"{region.name}: "
                    f"{old_weather} -> "
                    f"{new_weather}"
                )

                # =====================
                # SAVE WORLD STATE
                # =====================
                self.region_system.save_regions()

                # =====================
                # EMIT EVENT
                # =====================
                event_bus.emit(
                    "weather_changed",
                    {
                        "region": region,
                        "old_weather": old_weather,
                        "new_weather": new_weather
                    }
                )