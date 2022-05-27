import bspump

class JSONParserApp(bspump.BSPumpApplication):

    def __init__(self):
        super().__init__()

        from .service import ParserService
        self.ParserService = ParserService(self)