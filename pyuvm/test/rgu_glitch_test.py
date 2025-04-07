from rgu_pkg import *


@test()
class rgu_glitch_test(rgu_base_test):
    """Checking debounce system operation for sys_reset_n signal"""
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
        
        glitch_seq = rgu_reset_glitch_sequence("rgu_reset_glitch_sequence", self.cfg.clock_period)

        for _ in range(num_pkts):
            glitch_seq.randomize()
            await cocotb.start_soon(glitch_seq.start(self.env.sys_reset_n_agent.reset_seqr))
            await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, self.env.scoreboard.model.rgu_reg_timer0 + self.env.scoreboard.model.rgu_reg_timer1 + RESET_DELAY)
            await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_RST_STATUS_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))

        self.drop_objection()
