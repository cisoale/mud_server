class VnumManager:
    def __init__(self):
        self.current = 1000

    def next(self):
        self.current += 1
        return self.current

vnum_manager = VnumManager()