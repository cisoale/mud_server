from core.simulation.global_events import event_bus


def on_weather_changed(data):

    region = data["region"]

    print(
        f"[EVENT] "
        f"Meteo cambiato in "
        f"{region.name}"
    )


event_bus.subscribe(
    "weather_changed",
    on_weather_changed
)