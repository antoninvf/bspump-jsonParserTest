import logging
import bspump

#

L = logging.getLogger(__name__)


#

class ParseEventGenerator(bspump.Generator):
	async def generate(self, ctx, events, depth):
		for i in events:
			self.Pipeline.inject(ctx, i, depth)