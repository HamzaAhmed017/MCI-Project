from abc import ABC, abstractmethod


class Animation(ABC):
    def __init__(self, canvas):
        self.canvas = canvas
        self.running = False
        self.after_id = None

    def start(self):
        self.stop()
        self.running = True
        self.canvas.delete("all")
        self.setup()
        self.animate()

    def stop(self):
        self.running = False

        if self.after_id is not None:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None

    def reset(self):
        self.stop()
        self.canvas.delete("all")

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def animate(self):
        pass