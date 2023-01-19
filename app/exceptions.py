

class PostMessageException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else None

    def __str__(self):
        return self.message
