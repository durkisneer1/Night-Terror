
class BaseState:
    def __init__(self, app):
        self.app = app

    def handle_events(self, event):
        ...

    def update(self):
        ...

    def draw(self):
        ...
