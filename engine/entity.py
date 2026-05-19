class Entity:

    def __init__(self, entity_id, name):

        self.id = entity_id
        self.name = name

        self.components = {}

        self.tags = set()

        self.active = True

    # =========================
    # COMPONENTS
    # =========================

    def add_component(self, component):

        component_name = type(component).__name__

        self.components[component_name] = component

    def get_component(self, component_name):

        return self.components.get(component_name)

    def has_component(self, component_name):

        return component_name in self.components

    def remove_component(self, component_name):

        if component_name in self.components:
            del self.components[component_name]

    # =========================
    # TAGS
    # =========================

    def add_tag(self, tag):

        self.tags.add(tag)

    def has_tag(self, tag):

        return tag in self.tags

    def remove_tag(self, tag):

        self.tags.discard(tag)