import asab

from .service import ParserService


class ParserModule(asab.Module):
    def __init__(self, app):
        super().__init__(app)

        self.ParserService = ParserService(app)