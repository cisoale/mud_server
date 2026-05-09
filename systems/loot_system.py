def on_entity_killed(data):

    target = data["target"]

    generate_loot(target)

Registry.event_bus.subscribe(
    "entity_killed",
    on_entity_killed
)