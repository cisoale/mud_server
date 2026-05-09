import time


class TickSystem:

    def __init__(
        self,
        system,
        interval
    ):

        self.system = system
        self.interval = interval

        self.last_update = 0


class TickManager:

    def __init__(self):

        self.systems = []

    def register_system(
        self,
        system,
        interval
    ):

        self.systems.append(
            TickSystem(
                system,
                interval
            )
        )

    def update(self):

        now = time.time()

        for tick_system in self.systems:

            if (
                now - tick_system.last_update
                >= tick_system.interval
            ):

                tick_system.system.update()

                tick_system.last_update = now