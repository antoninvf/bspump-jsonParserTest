import logging
from datetime import datetime

import bspump

#

L = logging.getLogger(__name__)


#


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
