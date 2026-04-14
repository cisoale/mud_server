class Connection:

    def __init__(self, writer):
        self.writer = writer

    def send(self, text):
        try:
            self.writer.write(text.encode())
        except:
            pass