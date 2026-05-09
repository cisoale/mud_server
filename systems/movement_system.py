class MovementSystem:

    def move_entity(
        self,
        entity,
        new_room
    ):

        position = entity.get_component(
            "PositionComponent"
        )

        if not position:
            return False

        position.last_room_id = position.room_id
        position.room_id = new_room

        return True