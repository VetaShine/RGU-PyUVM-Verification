from rgu_pkg import *


@vsc.randobj
class rgu_simultaneous_resets_sequence(uvm_sequence):
    """Creating a reset signal with duration conditions"""
    def __init__(self, name):
        super().__init__(name)
        self.clk_cycles_after = vsc.rand_bit_t(32)
        self.clk_cycles_duration = vsc.rand_bit_t(32)

    @vsc.constraint
    def clk_cycles_constr(self):
        self.clk_cycles_after < RESET_COMFORT_DURATION_LIMIT
        self.clk_cycles_duration < SIMULTANEOUS_RESETS_DURATION_LIMIT_MAX and self.clk_cycles_duration > SIMULTANEOUS_RESETS_DURATION_LIMIT_MIN

    async def body(self):
        item = reset_driver_item(reset_action.RST_PULSE)
        item.clk_cycles_duration = self.clk_cycles_duration
        item.clk_cycles_after = self.clk_cycles_after
        
        await self.start_item(item)
        await self.finish_item(item)
