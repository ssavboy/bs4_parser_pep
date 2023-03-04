class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class Deferred:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def log(self, logger):
        for error_message in self.messages:
            logger(error_message)
