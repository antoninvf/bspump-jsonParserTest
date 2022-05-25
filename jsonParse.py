#!/usr/bin/env python3
from datetime import datetime
import logging

import bspump
import bspump.common
import bspump.file
import bspump.trigger
import bspump.kafka

#

L = logging.getLogger(__name__)


#

class ParserPipeline(bspump.Pipeline):
    def __init__(self, app, pipeline_id):
        super().__init__(app, pipeline_id)

        self.build(
            bspump.file.FileJSONSource(app, self).on(bspump.trigger.PeriodicTrigger(app, 5)),
            ParserProcessor(app, self),
            bspump.common.PPrintProcessor(app, self),
            bspump.common.StdDictToJsonParser(app, self),
            bspump.common.StringToBytesParser(app, self),
            bspump.kafka.KafkaSink(app, self, "KafkaConnection", id="KafkaSink")
        )


class ParserProcessor(bspump.Processor):

    def __init__(self, app, pipeline):
        super().__init__(app, pipeline)

    def process(self, ctx, events):
        devices = []
        for i in events:
            try:
                name = i['name']
                cpu_usage = i['state']['cpu']['usage']
                memory_usage = i['state']['memory']['usage']

                # conversion to UTC timestamp
                parsed_time = datetime.strptime(i['created_at'], "%Y-%m-%dT%H:%M:%S%z")
                created_at = int(datetime.utcfromtimestamp(parsed_time.timestamp()).timestamp())

                status = i['status']
                addresses = i['state']['network']['eth0']['addresses']  # shows all addresses from eth0 (ethernet port)

                parsed_json = {
                    'name': name,
                    'cpu_usage': cpu_usage,
                    'memory_usage': memory_usage,
                    'status': status,
                    'addresses': addresses,
                    'created_at': created_at,
                }
                devices.append(parsed_json)
            except TypeError:
                L.warning('The device had something missing --> skipped')

        return devices


if __name__ == '__main__':
    app = bspump.BSPumpApplication()
    svc = app.get_service("bspump.PumpService")

    kafka_connection = bspump.kafka.KafkaConnection(app, "KafkaConnection")
    svc.add_connection(kafka_connection)
    svc.add_pipeline(ParserPipeline(app, 'ParserPipeline'))

    app.run()
