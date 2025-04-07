from rgu_pkg import *


@vsc.randobj
class rgu_reset_glitch_sequence(uvm_sequence):
    """Creating a random glitch"""
    def __init__(self, name, period_time):
        super().__init__(name)
        self.time_duration = vsc.rand_bit_t(32)
        self.time_before = vsc.rand_bit_t(32)
        self.time_after = vsc.rand_bit_t(32)
        self.mode = mode_reset.ASYNC_MODE
        self.time_unit = 'ns'
        self.period_time = period_time

    @vsc.constraint
    def time_constr(self):
        self.time_duration < self.period_time / 4 # creating glitch
        self.time_before < 5 * self.period_time # just comfort limit
        self.time_after < 5 * self.period_time # just comfort limit

    async def body(self):
        item = reset_driver_item(reset_action.RST_PULSE)
        item.time_duration = self.time_duration
        item.time_before = self.time_before
        item.time_after = self.time_after
        item.mode = self.mode
        item.time_unit = self.time_unit
        
        await self.start_item(item)
        await self.finish_item(item)
