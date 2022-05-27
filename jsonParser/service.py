import bspump
import bspump.kafka

from .pipeline import ParserPipeline


class ParserService(bspump.BSPumpService):

    def __init__(self, app, service_name="jsonParser.ParserService"):
        super().__init__(app, service_name)

    async def initialize(self, app):
        svc = app.get_service("bspump.PumpService")

        # Create and register all pipelines/connections/matrices/lookups here

        kafka_connection = bspump.kafka.KafkaConnection(app, "KafkaConnection")
        svc.add_connection(kafka_connection)
        svc.add_pipeline(ParserPipeline(app, 'ParserPipeline'))

        await svc.initialize(app)