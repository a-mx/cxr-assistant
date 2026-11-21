from src.app.services.generator import Generator
class ModelRegistry:
    def __init__(self):
        self.generator = None

    def init_app(self, app):
        self.generator = Generator(
            app.config["GENERATOR_MODEL_PATH"]
        )