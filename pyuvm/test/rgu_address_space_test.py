from rgu_pkg import *


@test()
class rgu_address_space_test(rgu_base_test):
    """Checking access to registers and values by resetting"""
    async def apb_transactions(self, number, seq):
        """Generation of random APB transactions in a specified number"""
        for _ in range(number):
            seq.randomize()
            await cocotb.start_soon(seq.start(self.env.apb_agent.apb_master_seqr)) 
    
    async def reset_signals(self, massiv, flag, seq):
        """Sequential feeding of signals from an array with parameter randomization and checking values by reset"""
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_TIMER0_ADDR, data = RGU_TIM0, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_TIMER1_ADDR, data = RGU_TIM1, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_TIMER0_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_TIMER1_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
        
        if flag:
            await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = WDT_RESET_PERMISSION, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
        else:
            await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = WDT_RESET_PROHIBITION, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
        
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)

        for transaction_name in massiv:
            seq.randomize()
            await cocotb.start_soon(seq.start(getattr(self.env, transaction_name).reset_seqr))
            counter, timer0, timer1 = 0x0, getattr(self.env.scoreboard.model, f"rgu_reg_timer0"), getattr(self.env.scoreboard.model, f"rgu_reg_timer1")

            await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, timer0 + timer1 + RESET_DELAY)

            while counter <= RGU_REG_CPU_PWRUP_HEAVY_SWRST_ADDR:
                await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = counter, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
                counter += 4
        
    async def sw_signals(self, name):
        """Creating a reset from RGU_GLB.SW0/1_RESET and checking values by reset"""
        information = 0x2 if name == 'sw1_reset' else 0x1
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_TIMER0_ADDR, data = RGU_TIM0, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_TIMER1_ADDR, data = RGU_TIM1, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_TIMER0_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_TIMER1_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = information, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)

        counter = 0x0
        timer0 = RGU_TIM0 if name == 'sw0_reset' else getattr(self.env.scoreboard.model, f"rgu_reg_timer0")
        timer1 = RGU_TIM1 if name == 'sw0_reset' else getattr(self.env.scoreboard.model, f"rgu_reg_timer1")
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, timer0 + timer1 + RESET_DELAY)
        
        while counter <= RGU_REG_CPU_PWRUP_HEAVY_SWRST_ADDR:
            await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = counter, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
            counter += 4

    async def run_phase(self):
        """Initializing the system and running the script"""
        self.raise_objection()
        self.start_clock("cocotb_clock", self.cfg.clock_period)
        self.start_clock("cocotb_pclock", self.cfg.pclock_period)
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, SHORT_WAITING_DELAY)
        await cocotb.start_soon(rgu_reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = 20, clk_cycles_after = 20).start(self.env.sys_pwrgd_agent.reset_seqr))
        await cocotb.start_soon(rgu_reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = 20, clk_cycles_after = 20).start(self.env.apb_rst_agent.reset_seqr))
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, self.env.scoreboard.model.rgu_reg_timer0 + self.env.scoreboard.model.rgu_reg_timer1 + RESET_DELAY)

        try:
            num_pkts = int(cocotb.plusargs["num_pkts"])
        except KeyError:
            num_pkts = 10

        addr_space_seq = rgu_apb_space_sequence("rgu_apb_space_sequence")
        reset_space_seq = rgu_reset_space_sequence("rgu_reset_space_sequence")

        self.logger.info("Beginning the first part of the register access test")
        await self.apb_transactions(num_pkts, addr_space_seq)
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)
        self.logger.info("Beginning the first part of the reset register value test")
        await self.reset_signals(('wdt_rst_n_3_agent', 'wdt_rst_n_2_agent', 'wdt_rst_n_1_agent', 'wdt_rst_n_0_agent'), False, reset_space_seq)
        await self.reset_signals(('sys_reset_n_agent', 'sb_wdt_rst_n_agent', 'wdt_rst_n_3_agent', 'wdt_rst_n_2_agent', 'wdt_rst_n_1_agent', 'wdt_rst_n_0_agent', 'sys_pwrgd_agent'), True, reset_space_seq)    
        self.logger.info("Beginning the second part of the register access test")
        await self.apb_transactions(num_pkts, addr_space_seq)
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)
        self.logger.info("Beginning the second part of the reset register value test")
        await self.sw_signals('sw1_reset')
        await self.sw_signals('sw0_reset')
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)
        
        self.drop_objection()
