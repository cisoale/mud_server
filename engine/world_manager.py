class WorldManager:
    def __init__(self):
        self.entities = {}
        self.cities = {}
        self.caravans = {}

    def add_entity(self, entity):
        self.entities[entity.id] = entity

    def remove_entity(self, entity_id):
        if entity_id in self.entities:
            del self.entities[entity_id]