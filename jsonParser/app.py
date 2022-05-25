import bspump

class JSONParserApp(bspump.BSPumpApplication):

    def __init__(self):
        super().__init__()

        from .module import ParserModule
        self.add_module(ParserModule)