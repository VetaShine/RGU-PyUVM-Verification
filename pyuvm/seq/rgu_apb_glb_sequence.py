from rgu_pkg import *


@vsc.randobj
class rgu_apb_glb_sequence(uvm_sequence):
    """Randomization of data for the RGU_GLB registry"""
    def __init__(self, name):
        super().__init__(name)
        self.addr      = RGU_REG_GLB_ADDR
        self.data      = vsc.rand_bit_t(32)
        self.direction = apb_direction.WRITE
        self.pstrb     = 0xf

    @vsc.constraint
    def data_space_constr(self):
        self.data % 4 == 0 # the lowest two digits are guaranteed to be zeros to prevent unexpected resets

    async def body(self):
        item = apb_master_driver_item()
        item.addr = self.addr
        item.data = self.data
        item.direction = self.direction
        item.pstrb = self.pstrb
        
        await self.start_item(item)
        await self.finish_item(item)
