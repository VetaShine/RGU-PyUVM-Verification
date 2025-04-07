from rgu_pkg import *


@vsc.randobj
class rgu_apb_hold_sequence(uvm_sequence):
    """APB transaction randomization with conditions"""
    def __init__(self, name):
        super().__init__(name)
        self.addr      = vsc.rand_bit_t(32)
        self.data      = vsc.rand_bit_t(32)
        self.direction = vsc.rand_enum_t(apb_direction)
        self.pstrb     = 0xf

    @vsc.constraint
    def addr_space_constr(self):
        self.addr >= RGU_REG_SB_SWRST_ADDR 

    async def body(self):
        item = apb_master_driver_item()

        if self.addr > 0xfff:
            address = int((bin(self.addr)[2:-2] + '00')[-12:], 2)

            if address == RGU_REG_GLB_ADDR and self.direction == apb_direction.WRITE: # RGU_GLB register change prohibition to prevent unexpected resets
                item.addr = RGU_REG_RST_STATUS_ADDR
                item.data = self.data
            elif address == RGU_REG_RST_STATUS_ADDR and self.direction == apb_direction.READ: # prohibit reading from the register during reset
                item.addr = RGU_REG_GLB_ADDR
                item.data = self.data
            elif RGU_REG_TIMER0_ADDR <= address < RGU_REG_SB_SWRST_ADDR: # restrictions on large values for timers
                item.addr = self.addr
                item.data = random.randint(COMFORT_LIMIT_TIM_MIN, COMFORT_LIMIT_TIM_MAX)
            else:
                item.addr = self.addr
                item.data = self.data
        else:
            item.addr = self.addr
            item.data = self.data

        item.direction = self.direction
        item.pstrb = self.pstrb
        
        await self.start_item(item)
        await self.finish_item(item)
