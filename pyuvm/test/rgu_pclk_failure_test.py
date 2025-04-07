from rgu_pkg import *


@test()
class rgu_pclk_failure_test(rgu_base_test):
    """Verify system operation when pclk fails"""
    async def start_pclock(self, name, frequency):
        """Shaping pclock on/offs by random timing"""
        sig = getattr(cocotb.top, name)
        clock = cocotb.clock.Clock(sig, frequency, units="ns")
        self.task, self.work_flag = cocotb.start_soon(clock.start(start_high=False)), False    
        await cocotb.triggers.Timer(int((self.env.scoreboard.model.rgu_reg_timer0 + self.env.scoreboard.model.rgu_reg_timer1 + RESET_DELAY) * self.cfg.clock_period), units='ns')
        self.task.kill()
        
        while True:
            first_time, second_time = random.randint(1, int(self.cfg.clock_period * PCLK_FAILURE_TIME_LIMIT)), random.randint(1, int(self.cfg.clock_period * PCLK_FAILURE_TIME_LIMIT)) 
            
            if self.work_flag == False:
                self.task, self.work_flag = cocotb.start_soon(clock.start(start_high=False)), True

            await cocotb.triggers.Timer(first_time, units='ns')

            if self.work_flag == True:
                self.task.kill()
                self.work_flag = False

            await cocotb.triggers.Timer(second_time, units='ns')
    
    async def start_reset_processes(self, num_pkts, seq):
        """Formation of random resets in a set amount"""
        for _ in range(num_pkts):
            reset_element = random.choice(self.reset_signals)
            seq.randomize()
            await cocotb.start_soon(seq.start(getattr(self.env, reset_element).reset_seqr))
            await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, self.env.scoreboard.model.rgu_reg_timer0 + self.env.scoreboard.model.rgu_reg_timer1 + RESET_DELAY)
            
            if random.randint(0, 1) == 1 and not self.work_flag == True:
                await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = WDT_RESET_PERMISSION, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
    
    async def start_sw_processes(self, num_pkts):
        """Formation of reset by writing to the register RGU_GLB.SW0/1_RESET in a set amount"""
        stop_flag, counter = False, 0

        while not stop_flag:
            if self.work_flag == True:
                await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = random.randint(1, 2), direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))

                if counter == 0:
                    self.task.kill()
                    self.work_flag = False

                await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, self.env.scoreboard.model.rgu_reg_timer0 + self.env.scoreboard.model.rgu_reg_timer1 + RESET_DELAY)
                counter += 1
            else:
                await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, SHORT_WAITING_DELAY)
            
            if counter == num_pkts:
                stop_flag = True

    async def run_phase(self):
        """Initializing the system and running the script"""
        self.raise_objection()
        self.pclk_flag = False
        self.start_clock("cocotb_clock", self.cfg.clock_period)
        cocotb.start_soon(self.start_pclock("cocotb_pclock", self.cfg.pclock_period))
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, SHORT_WAITING_DELAY)
        await cocotb.start_soon(rgu_reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = 20, clk_cycles_after = 20).start(self.env.sys_pwrgd_agent.reset_seqr))
        await cocotb.start_soon(rgu_reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = 20, clk_cycles_after = 20).start(self.env.apb_rst_agent.reset_seqr))
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, self.env.scoreboard.model.rgu_reg_timer0 + self.env.scoreboard.model.rgu_reg_timer1 + RESET_DELAY)

        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = WDT_RESET_PERMISSION, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)

        try:
            num_pkts = int(cocotb.plusargs["num_pkts"])
        except KeyError:
            num_pkts = 10

        self.reset_signals = ['sys_pwrgd_agent', 'sys_reset_n_agent', 'sb_wdt_rst_n_agent', 'wdt_rst_n_3_agent', 'wdt_rst_n_2_agent', 'wdt_rst_n_1_agent', 'wdt_rst_n_0_agent']
        reset_space_seq = rgu_reset_space_sequence("rgu_reset_space_sequence")

        await self.start_reset_processes(num_pkts, reset_space_seq)
        self.logger.info("Start to check SW0/1 resets")
        await self.start_sw_processes(num_pkts)

        self.drop_objection()
