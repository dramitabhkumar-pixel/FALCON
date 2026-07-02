from core.base_engine import BaseEngine


class TestEngine(BaseEngine):

    def __init__(self):

        super().__init__("Test")

    def validate(self, data):

        return True

    def run(self, data):

        self.log("Running")

        return data


engine = TestEngine()

print(engine.run(100))