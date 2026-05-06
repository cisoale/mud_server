class EventBus:

    def __init__(self):

        self.listeners = {}

    # =========================
    # SUBSCRIBE
    # =========================
    def subscribe(self, event_name, callback):

        if event_name not in self.listeners:
            self.listeners[event_name] = []

        self.listeners[event_name].append(callback)

    # =========================
    # EMIT
    # =========================
    def emit(self, event_name, data=None):

        callbacks = self.listeners.get(event_name, [])

        for callback in callbacks:

            try:
                callback(data)

            except Exception as e:

                print(
                    f"[EVENT BUS ERROR] "
                    f"{event_name}: {e}"
                )