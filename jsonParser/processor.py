import logging
from datetime import datetime

import bspump

#

L = logging.getLogger(__name__)


#


class ParserProcessor(bspump.Processor):
    def __init__(self, app, pipeline):
        super().__init__(app, pipeline)

    def process(self, ctx, e):
        name = e.get('name')

        if e.get('state') is not None:
            if e.get('state').get('cpu') is not None: cpu_usage = e.get('state').get('cpu').get('usage')
            else: cpu_usage = None
            if e.get('state').get('memory') is not None: memory_usage = e.get('state').get('memory').get('usage')
            else: memory_usage = None

            # shows all addresses from eth0 (ethernet port)
            if e.get('state').get('network') is not None:
                if e.get('state').get('network').get('eth0') is not None: addresses = e.get('state').get('network').get('eth0').get('addresses')
                else: addresses = None
            else: addresses = None

        else: cpu_usage = None; memory_usage = None; addresses = None

        # conversion to UTC timestamp
        if e.get('created_at') is not None:
            parsed_time = datetime.strptime(e.get('created_at'), "%Y-%m-%dT%H:%M:%S%z")
            created_at = int(datetime.utcfromtimestamp(parsed_time.timestamp()).timestamp())
        else: created_at = None

        status = e.get('status')


        parsed_json = {
            'name': name,
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'status': status,
            'addresses': addresses,
            'created_at': created_at,
        }
        return parsed_json
