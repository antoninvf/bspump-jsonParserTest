#!/usr/bin/env python3
import bspump
import bspump.common
import bspump.file
import bspump.trigger
import bspump.kafka

from .processor import ParserProcessor
from .generator import ParseEventGenerator

class ParserPipeline(bspump.Pipeline):

    def __init__(self, app, pipeline_id):
        super().__init__(app, pipeline_id)

        self.build(
            bspump.file.FileJSONSource(app, self).on(bspump.trigger.PeriodicTrigger(app, 5)),
            ParseEventGenerator(app, self),
            ParserProcessor(app, self),
            bspump.common.PPrintProcessor(app, self),
            bspump.common.StdDictToJsonParser(app, self),
            bspump.common.StringToBytesParser(app, self),
            bspump.kafka.KafkaSink(app, self, "KafkaConnection", id="KafkaSink")
        )


