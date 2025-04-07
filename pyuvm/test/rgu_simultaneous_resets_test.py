from rgu_pkg import *


@test()
class rgu_simultaneous_resets_test(rgu_base_test):
    """Check system operation during simultaneous reset signals, after global reset and reset hold test"""
    async def apb_transactions(self):
        """Generation of random APB transactions"""
        while True:
            self.apb_hold_seq.randomize()
            await cocotb.start_soon(self.apb_hold_seq.start(self.env.apb_agent.apb_master_seqr))
    
    async def check_simultaneous_reset_requests(self):
        """Simultaneous reset signals"""
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = SIMULTANEOUS_SW_RESETS, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, RGU_TIM0 + RGU_TIM1 + RESET_DELAY)
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_RST_STATUS_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)

        for _ in range(self.num_pkts):
            random_count = random.randint(SIMULTANEOUS_MIN_COUNT, SIMULTANEOUS_MAX_COUNT)
            selected_elements = random.sample(self.reset_signals, random_count)

            tasks = []

            for name in selected_elements:
                self.reset_seq.randomize()
                tasks.append(cocotb.start_soon(self.reset_seq.start(getattr(self.env, name).reset_seqr)))
            
            await cocotb.triggers.Combine(*tasks)
            await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, self.env.scoreboard.model.rgu_reg_timer0 + self.env.scoreboard.model.rgu_reg_timer1 + RESET_DELAY)

            await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_RST_STATUS_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
            await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)

            if random.randint(0, 1) == 1:
                self.apb_glb_seq.randomize()
                await cocotb.start_soon(self.apb_glb_seq.start(self.env.apb_agent.apb_master_seqr))
                await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
                await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)
    
    async def check_after_glb_duration(self):
        """Sys_reset_n signal after sys_pwrgd"""
        for _ in range(self.num_pkts):
            self.reset_seq.randomize()
            number = random.randint(MIN_CYCLES_COUNT_AFTER_GLB, MAX_CYCLES_COUNT_AFTER_GLB)
            sys_reset_duration = random.randint(number, self.reset_seq.clk_cycles_duration) if number < self.reset_seq.clk_cycles_duration else number
            cocotb.start_soon(self.reset_seq.start(self.env.sys_pwrgd_agent.reset_seqr))
            await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, self.reset_seq.clk_cycles_duration + number - sys_reset_duration)
            cocotb.start_soon(rgu_reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = sys_reset_duration, clk_cycles_after = random.randint(0, RESET_COMFORT_DURATION_LIMIT)).start(self.env.sys_reset_n_agent.reset_seqr))
            await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, RGU_TIM0 + RGU_TIM1 + RESET_DELAY + sys_reset_duration)
            await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_RST_STATUS_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
            await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)
    
    async def check_soc_hold_in_reset(self):
        """Submit APB transactions while the reset signal level is active"""
        await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_GLB_ADDR, data = WDT_RESET_PERMISSION, direction = apb_direction.WRITE).start(self.env.apb_agent.apb_master_seqr))
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)

        for _ in range(self.num_pkts):
            selected_element = random.choice(self.hold_reset_signals)
            self.reset_seq.randomize()
            timer0, timer1 = getattr(self.env.scoreboard.model, f"rgu_reg_timer0"), getattr(self.env.scoreboard.model, f"rgu_reg_timer1")
            time = self.reset_seq.clk_cycles_duration if selected_element.startswith('sys') else min(timer0, self.reset_seq.clk_cycles_duration)
            after_time = timer0 + timer1 + RESET_DELAY + APB_DELAY if selected_element.startswith('sys') else max(timer0 + timer1 + RESET_DELAY, self.reset_seq.clk_cycles_duration + RESET_DELAY)
            cocotb.start_soon(self.reset_seq.start(getattr(self.env, selected_element).reset_seqr))

            if time - APB_DELAY > 0:
                await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, RESET_DELAY + 1)
                task = cocotb.start_soon(self.apb_transactions())
                await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, time - APB_DELAY)
                task.kill()
            else:
                after_time += time
            
            timer0, timer1 = getattr(self.env.scoreboard.model, f"rgu_reg_timer0"), getattr(self.env.scoreboard.model, f"rgu_reg_timer1")
            second_after_time = timer0 + timer1 + RESET_DELAY + APB_DELAY if selected_element.startswith('sys') else max(timer0 + timer1 + RESET_DELAY, self.reset_seq.clk_cycles_duration + RESET_DELAY)

            if after_time > second_after_time:
                await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, after_time)
            else:
                await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, second_after_time)
        
            await cocotb.start_soon(rgu_apb_sequence_param("apb_param_stim", addr = RGU_REG_RST_STATUS_ADDR, data = 0x0, direction = apb_direction.READ).start(self.env.apb_agent.apb_master_seqr))
            await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, APB_DELAY)

    
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
            self.num_pkts = int(cocotb.plusargs["num_pkts"])
        except KeyError:
            self.num_pkts = 10

        self.reset_signals = ['sys_pwrgd_agent', 'sys_reset_n_agent', 'sb_wdt_rst_n_agent', 'wdt_rst_n_3_agent', 'wdt_rst_n_2_agent', 'wdt_rst_n_1_agent', 'wdt_rst_n_0_agent']
        self.hold_reset_signals = ['sys_reset_n_agent', 'sb_wdt_rst_n_agent', 'wdt_rst_n_3_agent', 'wdt_rst_n_2_agent', 'wdt_rst_n_1_agent', 'wdt_rst_n_0_agent']
        self.reset_seq = rgu_simultaneous_resets_sequence("rgu_simultaneous_resets_sequence")
        self.apb_glb_seq, self.apb_hold_seq = rgu_apb_glb_sequence("rgu_apb_glb_sequence"), rgu_apb_hold_sequence("rgu_apb_hold_sequence")

        self.logger.info("Start to check simultaneous reset requests")
        await self.check_simultaneous_reset_requests()
        self.logger.info("Start to check after glb duration")
        await self.check_after_glb_duration()
        self.logger.info("Start to check soc hold in reset")
        await self.check_soc_hold_in_reset()

        self.drop_objection()
