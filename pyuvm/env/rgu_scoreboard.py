from rgu_pkg import *

    
class rgu_scoreboard(uvm_component):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.assert_counter, self.deassert_counter, self.check_err_off, self.error_count, self.reset_count, self.apb_count, self.wrong_transactions_count = 0, 0, 0, 0, 0, 0, 0
        self.cold_reset_flag, self.reset_flag, self.reset_occurs_flag, self.sys_pwrgd_end_flag, self.sys_reset_n_wait_flag, self.no_check_flag, self.five_flag, self.high_duration_flag = True, False, False, False, False, False, False, False
        self.sb_registers = ['sb_dmac_n', 'sb_qspi_n', 'sb_i2c_n_0', 'sb_i2c_n_1', 'sb_uart_n', 'sb_gpio_n', 'sb_sram_n']
        self.stage0 = ['sb_sys_n', 'sb_dmac_n', 'sb_qspi_n', 'sb_i2c_n_1', 'sb_i2c_n_0', 'sb_uart_n', 'sb_gpio_n', 'sb_sram_n']
        self.priority_map = {'sys_pwrgd':0, 'sys_reset_n':1, 'sb_wdt_rst_n':2, 'sw0_reset':3, 'sw1_reset':4, 'wdt_rst_n_3':5, 'wdt_rst_n_2':5, 'wdt_rst_n_1':5, 'wdt_rst_n_0':5}
        self.priority_queue = cocotb.queue.PriorityQueue()
        self.reset_queue, self.registers_queue = cocotb.queue.Queue(), cocotb.queue.Queue()
        self.sys_pwrgd_transaction, self.sys_pwrgd_deassert_transaction, self.task = None, None, None
        self.max_num_err = int(os.environ.get('MAX_QUIT_COUNT'))

        for key in self.priority_map:
            if not key.startswith('sw'):
                setattr(self, f"{key}_deassert_queue", cocotb.queue.Queue())

    def build_phase(self):
        for key, value in reset_agent_names.items():
            setattr(self, f'{key}_fifo_reset', uvm_tlm_analysis_fifo(f"{key}_fifo_reset", self))

        self.apb_fifo_trans = uvm_tlm_analysis_fifo("apb_fifo_trans", self)

    def is_error(self, name_error = None):
        """Counting the number of errors and terminating the simulation when the limit is reached"""
        self.error_count += 1

        if name_error is not None:
            self.logger.error(name_error)

        if self.error_count > self.max_num_err:
            raise RuntimeError(f"Maximum errors count reached: {self.max_num_err} errors")
    
    def set_rgu_env_cfg(self, rgu_env_cfg):
        """Providing access to the environment configuration"""
        self.__rgu_env_cfg = rgu_env_cfg

    async def deassert_waiting(self, key):
        """Waiting for DEASSERT signal for incoming ASSERT reset signal"""
        self.reset_count += 1
        deassert_transaction = await getattr(self, f"{key}_deassert_queue").get()
        self.reset_count -= 1
        return deassert_transaction[1]
    
    async def process_start(self):
        """Processing the received reset signal and starting resetting"""
        if not self.priority_queue.empty():
            self.sample_scoreboard(0)
            copied_priority_queue = copy.deepcopy(self.priority_queue)
            self.priority_queue = cocotb.queue.PriorityQueue()
            name, wdt_rst_flag, self.sys_reset_n_flag, after_glb_flag, deassert_transaction = copied_priority_queue.get_nowait()[1], False, False, False, None

            if name.startswith('w'):
                self.sample_scoreboard(1)
                rgu_glb_string, flag = bin(self.model.rgu_reg_glb)[2:].zfill(6), False

                while not flag:
                    if rgu_glb_string[-(int(name[-1]) + 3)] != '1': # checking whether a discharge authorisation is in place 
                        self.sample_scoreboard(2)
                        cocotb.start_soon(self.deassert_waiting(name))

                        if not copied_priority_queue.empty():
                            self.sample_scoreboard(3)
                            name = copied_priority_queue.get_nowait()[1]
                        else:
                            self.sample_scoreboard(4)
                            wdt_rst_flag, flag, self.reset_flag = True, True, False
                    else:
                        self.sample_scoreboard(5)
                        flag = True
            
            while not copied_priority_queue.empty():
                naming = copied_priority_queue.get_nowait()[1]

                if not naming.startswith('sw'):
                    self.sample_scoreboard(6)
                    cocotb.start_soon(self.deassert_waiting(naming))
            
            if not name.startswith('sw'):
                self.sample_scoreboard(7)
                transaction = getattr(self, f"{name}_dut_trn")

            if self.reset_occurs_flag == True: # branch to check sys_reset_n after sys_pwrgd
                self.sample_scoreboard(8)

                if name == 'sys_reset_n' and not self.sys_pwrgd_transaction is None:
                    self.sample_scoreboard(9)
                    self.sys_reset_n_wait_flag, self.sys_reset_n_flag = True, True
                    deassert_transaction = await self.deassert_waiting(name)
                    pwrgd_end_flag = self.sys_pwrgd_end_flag
                    await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, 2)
                    duration = deassert_transaction.time_assert - self.sys_pwrgd_deassert_transaction.time_assert

                    if self.sys_pwrgd_end_flag == False:
                        self.sample_scoreboard(10)
                        await self.task

                        if duration > RESET_DURATION_LIMIT_MIN * self.__rgu_env_cfg.clock_period or math.isclose(RESET_DURATION_LIMIT_MIN * self.__rgu_env_cfg.clock_period, duration):
                            self.sample_scoreboard(11)

                            if self.wrong_transactions_count == 0 and not math.isclose(RESET_DURATION_LIMIT_MIN * self.__rgu_env_cfg.clock_period, duration):
                                self.is_error("There was no reset after a global reset with the correct duration of the sys_reset_n signal")
                            else:
                                self.sample_scoreboard(12)
                                self.wrong_transactions_count = 0
                        elif self.wrong_transactions_count != 0:
                            self.is_error(f"There was a reset after a global reset when the duration of the sys_reset_n signal was incorrect. Number of transactions at incorrect time = {self.wrong_transactions_count}")
                            self.wrong_transactions_count = 0
                    elif duration > RESET_DURATION_LIMIT_MIN * self.__rgu_env_cfg.clock_period or math.isclose(RESET_DURATION_LIMIT_MIN * self.__rgu_env_cfg.clock_period, duration):
                        self.sample_scoreboard(13)

                        if math.isclose(RESET_DURATION_LIMIT_MIN * self.__rgu_env_cfg.clock_period, duration) or pwrgd_end_flag != self.sys_pwrgd_end_flag:
                            self.sample_scoreboard(14)
                            self.five_flag = True
                        
                        if RGU_TIM0 + RGU_TIM1 + SYS_RESET_N_DELAY > RESET_DURATION_LIMIT_MIN:
                            self.sample_scoreboard(15)
                            self.high_duration_flag = True
                        
                        self.sys_reset_n_flag, self.no_check_flag = False, True
                    self.sys_reset_n_wait_flag = False
                else:
                    self.is_error(f"During the reset, a request for another reset from {name} came in")

            if name == 'sys_pwrgd':
                self.sample_scoreboard(16)
                self.model = rgu_model()
            elif name == 'sw0_reset':
                self.sample_scoreboard(17)
                self.model = rgu_model()
                self.model.rgu_reg_rst_status = RGU_RST_STATUS_SW0_RESET
            elif name == 'sw1_reset':
                self.sample_scoreboard(18)
                self.model.rgu_reg_glb -= 0x2 # zeroing of the second digit called SW1_RESET
                self.model.rgu_reg_rst_status = RGU_RST_STATUS_SW1_RESET
            
            if name.startswith('sw'):
                self.sample_scoreboard(19)
                await self.sw_process(name)
            elif wdt_rst_flag != True and self.sys_reset_n_flag != True:
                self.sample_scoreboard(20)
                self.task = cocotb.start_soon(self.reset_process(name, transaction, deassert_transaction))
                await self.task
    
    async def sw_process(self, name):
        """Reset processing by register write RGU_GLB.SW0/1_RESET"""
        self.reset_count, stop_flag, self.assert_counter, self.deassert_counter, sw_time, timer0, timer1 = self.reset_count + 1, False, 0, 0, None, self.model.rgu_reg_timer0, self.model.rgu_reg_timer1

        while not stop_flag:
            new_transaction = await self.registers_queue.get()

            if new_transaction[0] != 'apb_rst' and new_transaction[1].rst_st == rst_state.RST_ASSERT:
                self.sample_scoreboard(21)
                self.assert_counter += 1

                if sw_time is None:
                    self.sample_scoreboard(22)
                    sw_time = new_transaction[1].time_assert
            elif new_transaction[0] != 'apb_rst':
                self.sample_scoreboard(23)
                self.deassert_counter += 1

                if new_transaction[0] in self.stage0:
                    self.sample_scoreboard(24)

                    if not math.isclose(new_transaction[1].time_assert, sw_time + timer0 * self.__rgu_env_cfg.clock_period):
                        self.is_error(f'Wrong time for {new_transaction[0]} transaction: {new_transaction[1]}')
                else:
                    self.sample_scoreboard(25)

                    if not math.isclose(new_transaction[1].time_assert, sw_time + (timer0 + timer1) * self.__rgu_env_cfg.clock_period):
                        self.is_error(f'Wrong time for {new_transaction[0]} transaction: {new_transaction[1]}')
            
            if (name == 'sw1_reset' and self.assert_counter == self.deassert_counter != 0) or (name == 'sw0_reset' and self.deassert_counter == CLASSIC_DEASSERT_COUNT):
                self.sample_scoreboard(26)
                stop_flag, self.reset_count = True, self.reset_count - 1

    async def check_assert_transaction(self, name, main_transaction, checked_transaction):
        """Checking the ASSERT signal time"""
        if name == 'sys_pwrgd':
            self.sample_scoreboard(27)
            
            if not math.isclose(checked_transaction[1].time_assert, main_transaction.time_assert):
                self.is_error(f'Wrong time for {checked_transaction[0]} transaction: {checked_transaction[1]}')
        else:
            self.sample_scoreboard(28)

            if not math.isclose(checked_transaction[1].time_assert, main_transaction.time_assert + ASSERT_DELAY * self.__rgu_env_cfg.clock_period):
                self.is_error(f'Wrong time for {checked_transaction[0]} transaction: {checked_transaction[1]}')
    
    async def deassert_comparison(self, flag, checked_transaction, main_time, time0, time1, value):
        """Comparison of received and expected DEASSERT signal timing"""
        if flag == False and not math.isclose(checked_transaction[1].time_assert, main_time + (time0 + value) * self.__rgu_env_cfg.clock_period):
            self.sample_scoreboard(29)

            if self.sys_reset_n_flag == True:
                self.sample_scoreboard(30)
                self.wrong_transactions_count += 1
            else:
                self.is_error(f'Wrong time for {checked_transaction[0]} transaction: {checked_transaction[1]}')
        elif flag == True and not math.isclose(checked_transaction[1].time_assert, main_time + (time0 + time1 + value) * self.__rgu_env_cfg.clock_period):
            self.sample_scoreboard(31)

            if self.sys_reset_n_flag == True:
                self.sample_scoreboard(32)
                self.wrong_transactions_count += 1
            else:
                self.is_error(f'Wrong time for {checked_transaction[0]} transaction: {checked_transaction[1]}')
    
    async def check_deassert_transaction(self, name, main_transaction, checked_transaction, time0, time1):
        """Checking the DEASSERT signal time"""
        stage_flag = False if checked_transaction[0] in self.stage0 else True

        if main_transaction is None:
            self.is_error(f'Wrong time for {checked_transaction[0]} transaction: {checked_transaction[1]}')
        elif name == 'sys_pwrgd':
            self.sample_scoreboard(33)
            await self.deassert_comparison(stage_flag, checked_transaction, main_transaction.time_assert, time0, time1, SYS_PWRGD_DELAY)
        elif name == 'sys_reset_n':
            self.sample_scoreboard(34)
            await self.deassert_comparison(stage_flag, checked_transaction, main_transaction.time_assert, time0, time1, SYS_RESET_N_DELAY)
        else:
            self.sample_scoreboard(35)
            await self.deassert_comparison(stage_flag, checked_transaction, main_transaction.time_assert, time0, time1, WDT_DELAY)
    
    async def change_registers(self, name):
        """Change the RGU_RST_STATUS register to the source of the reset in progress"""
        if name == 'sys_reset_n':
            self.sample_scoreboard(36)
            self.model.rgu_reg_rst_status = RGU_RST_STATUS_SYS_RESET
        elif name == 'sb_wdt_rst_n':
            self.sample_scoreboard(37)
            self.model.rgu_reg_rst_status = RGU_RST_STATUS_SB_WDT_RESET
        elif name.startswith('w'):
            self.sample_scoreboard(38)
            self.model.rgu_reg_rst_status = RGU_RST_STATUS_SYS_WDT_RESET

    async def reset_process(self, name, transaction, dst_transaction):
        """Resetting process"""
        self.sys_pwrgd_deassert_transaction = None

        if name == 'sys_pwrgd':
            self.sample_scoreboard(39)
            self.sys_pwrgd_end_flag = False
            self.sys_pwrgd_transaction = copy.deepcopy(transaction)
        
        if self.cold_reset_flag == True:
            self.sample_scoreboard(40)
            self.assert_counter = CLASSIC_DEASSERT_COUNT
        else:
            self.sample_scoreboard(41)
            self.assert_counter = 0

        self.reset_count, self.reset_occurs_flag, stop_flag, self.deassert_counter, time0, time1 = self.reset_count + 1, True, False, 0, self.model.rgu_reg_timer0, self.model.rgu_reg_timer1
        deassert_transaction = await self.deassert_waiting(name) if dst_transaction is None else copy.deepcopy(dst_transaction) 
        main_transaction = transaction if (name.startswith('sb') or name.startswith('w')) else copy.deepcopy(deassert_transaction)
        duration = deassert_transaction.time_assert - transaction.time_assert
        integer_duration = int(round(duration / self.__rgu_env_cfg.clock_period))

        if name == 'sys_pwrgd':
            self.sample_scoreboard(42)
            self.sys_pwrgd_deassert_transaction = copy.deepcopy(deassert_transaction)

        if RESET_DURATION_LIMIT_MIN + 2 - integer_duration > 0:
            self.sample_scoreboard(43)
            await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, RESET_DURATION_LIMIT_MIN + 2 - integer_duration)

        if (name == 'sys_reset_n' and duration < self.__rgu_env_cfg.clock_period / 4) or ((name.startswith('sb') or name.startswith('w')) and integer_duration < WDT_EXACT_DURATION_LIMIT):
            self.sample_scoreboard(44)

            if not self.reset_queue.empty():
                if name == 'sys_reset':
                    self.is_error(f"Reset on {name} transaction with incorrect active time = {duration}: {transaction}")
                else:
                    self.is_error(f"Reset on {name} transaction with incorrect active levels = {integer_duration}: {transaction}")
            else:
                self.sample_scoreboard(45)
                stop_flag, self.reset_flag, self.reset_count, self.reset_occurs_flag = True, False, self.reset_count - 1, False
        elif self.cold_reset_flag != True and self.reset_queue.empty() and self.five_flag != True:
            self.is_error(f"No reset for {name} with active time = {duration}: {transaction}")
            stop_flag, self.reset_count, self.reset_occurs_flag, self.sys_pwrgd_transaction, self.five_flag, self.high_duration_flag, self.no_check_flag = True, self.reset_count - 1, False, None, False, False, False

            if name == 'sys_pwrgd':
                self.sys_pwrgd_end_flag = True
            
            await self.change_registers(name)
        elif self.high_duration_flag != True:
            self.sample_scoreboard(46)
            await self.change_registers(name)

        while not stop_flag:
            new_transaction = await self.reset_queue.get()

            if new_transaction[0] != 'apb_rst' and new_transaction[1].rst_st == rst_state.RST_ASSERT:
                self.sample_scoreboard(47)
                self.assert_counter += 1

                if self.sys_reset_n_flag != True and self.no_check_flag != True:
                    self.sample_scoreboard(48)
                    await self.check_assert_transaction(name, transaction, new_transaction)
            elif new_transaction[0] != 'apb_rst' and new_transaction[1].rst_st == rst_state.RST_DEASSERT and new_transaction[0] not in self.priority_map:
                self.sample_scoreboard(49)
                self.deassert_counter += 1

                if self.cold_reset_flag != True and self.no_check_flag != True:
                    self.sample_scoreboard(50)
                    await self.check_deassert_transaction(name, main_transaction, new_transaction, time0, time1)
            
            if self.assert_counter == self.deassert_counter != 0 or (name == 'sys_pwrgd' and self.deassert_counter == CLASSIC_DEASSERT_COUNT and self.sys_reset_n_wait_flag != True):
                self.sample_scoreboard(51)
                stop_flag, self.reset_count, self.reset_occurs_flag, self.sys_pwrgd_transaction, self.no_check_flag, self.five_flag, self.high_duration_flag = True, self.reset_count - 1, False, None, False, False, False
                
                if self.sys_reset_n_wait_flag != True:
                    self.sample_scoreboard(52)
                    self.reset_flag = False
                
                if self.cold_reset_flag == True:
                    self.sample_scoreboard(53)
                    self.cold_reset_flag = False
                elif name == 'sys_pwrgd':
                    self.sample_scoreboard(54)
                    self.sys_pwrgd_end_flag = True
    
    async def get_rst_dut_trn(self, key):
        """Processing a received reset transaction"""
        while True:
            setattr(self, f"{key}_dut_trn", await (getattr(self, f"{key}_fifo_reset")).get())

            if key in self.priority_map and getattr(self, f"{key}_dut_trn").rst_st == rst_state.RST_ASSERT:
                self.sample_scoreboard(55)
                self.reset_flag = True
                self.priority_queue.put_nowait((self.priority_map[key], key))
                await cocotb.triggers.Timer(0.1, 'ns')

                if not self.priority_queue.empty():
                    self.sample_scoreboard(56)
                    cocotb.start_soon(self.process_start())
            elif key in self.priority_map and getattr(self, f"{key}_dut_trn").rst_st == rst_state.RST_DEASSERT:
                self.sample_scoreboard(57)
                getattr(self, f"{key}_deassert_queue").put_nowait((key, getattr(self, f"{key}_dut_trn")))
            elif self.reset_flag == True:
                self.sample_scoreboard(58)
                self.reset_queue.put_nowait((key, getattr(self, f"{key}_dut_trn")))
            elif key not in self.priority_map:
                self.sample_scoreboard(59)
                self.registers_queue.put_nowait((key, getattr(self, f"{key}_dut_trn")))

    async def get_apb_dut_trn(self):
        """Waiting for APB transaction and starting its processing upon receipt"""
        while True:
            self.apb_dut_trn = await self.apb_fifo_trans.get()
            await self.check_apb_trn(self.apb_dut_trn)
    
    async def symbol_comparison(self, previous_symbol, new_symbol, key):
        """Comparison of previous and new discharge values"""
        self.apb_count += 1
        expected_transaction = await self.registers_queue.get()

        while key != expected_transaction[0]:
            previous_transaction = copy.deepcopy(expected_transaction)
            expected_transaction = await self.registers_queue.get()
            self.registers_queue.put_nowait(previous_transaction)

        if previous_symbol < new_symbol and expected_transaction[1].rst_st != rst_state.RST_ASSERT:
            self.is_error(f"Wrong transaction status for {key}")
        elif previous_symbol > new_symbol and expected_transaction[1].rst_st != rst_state.RST_DEASSERT:
            self.is_error(f"Wrong transaction status for {key}")
        else:
            self.sample_scoreboard(60)
        
        self.apb_count -= 1

    async def transaction_waiting(self, previous_value, new_value, address):
        """Checking register changes to wait for receiving signals from channels"""
        if self.model.addresses[address][2] == 1:
            self.sample_scoreboard(61)
            cocotb.start_soon(self.symbol_comparison(previous_value, new_value, f"{self.model.addresses[address][0][8:-6]}_n"))

            if address == RGU_REG_SYS_SWRST_ADDR:
                self.sample_scoreboard(62)

                for number in range(4):
                    cocotb.start_soon(self.symbol_comparison(previous_value, new_value, f"wdt_n_{number}"))

                for number in range(8):
                    cocotb.start_soon(self.symbol_comparison(previous_value, new_value, f"gpt_n_{number}"))
        else:
            self.sample_scoreboard(63)
            waiting_counter = 0

            for symbol in previous_value[::-1]:
                if symbol != new_value[waiting_counter]:
                    self.sample_scoreboard(64)

                    if address == RGU_REG_SB_SWRST_ADDR:
                        self.sample_scoreboard(65)
                        cocotb.start_soon(self.symbol_comparison(symbol, new_value[waiting_counter], self.sb_registers[waiting_counter]))
                    else:
                        self.sample_scoreboard(66)
                        cocotb.start_soon(self.symbol_comparison(symbol, new_value[waiting_counter], f"{self.model.addresses[address][0][8:-6]}_n_{waiting_counter}"))
                
                waiting_counter += 1

    async def check_apb_trn(self, apb_dut_trn):
        """APB transaction processing"""
        address = bin(int(apb_dut_trn.address, 16))[2:-2] + '00'

        if int(address, 2) > 0xffc: # more than 12 bits after zeroing the two low-order bits
            self.sample_scoreboard(67)
            address = int(address[-12:], 2)
        else:
            self.sample_scoreboard(68)
            address = int(address, 2)

        if address > RGU_REG_CPU_PWRUP_HEAVY_SWRST_ADDR:
            self.sample_scoreboard(69)

            if apb_dut_trn.pslverr_enable != 1:
                self.is_error(f"Invalid APB-transaction has no PSLV_ERR=1 {apb_dut_trn}")
        else:
            self.sample_scoreboard(70)

            if apb_dut_trn.pslverr_enable == 1:
                self.is_error(f"Valid APB-transaction has PSLV_ERR=1 {apb_dut_trn}")
            elif self.check_err_off == 0:
                self.sample_scoreboard(71)

                if apb_dut_trn.direction == apb_direction.WRITE and self.model.addresses[address][1] == 'rw':
                    self.sample_scoreboard(72)
                    previous_value = (bin(getattr(self.model, self.model.addresses[address][0]))[2:]).zfill(self.model.addresses[address][2])
                    setattr(self.model, self.model.addresses[address][0], int(((bin(apb_dut_trn.data)[2:]).zfill(APB_CAPACITY))[APB_CAPACITY - self.model.addresses[address][2]:], 2))
                    new_value = bin(getattr(self.model, self.model.addresses[address][0]))[2:].zfill(self.model.addresses[address][2])

                    if address == RGU_REG_GLB_ADDR:
                        self.sample_scoreboard(73)

                        if bin(self.model.rgu_reg_glb)[2:][-1] == '1':
                            self.sample_scoreboard(74)
                            self.priority_queue.put_nowait((self.priority_map['sw0_reset'], 'sw0_reset'))
                            cocotb.start_soon(self.process_start())
                        elif bin(self.model.rgu_reg_glb)[2:].zfill(2)[-2] == '1':
                            self.sample_scoreboard(75)
                            self.priority_queue.put_nowait((self.priority_map['sw1_reset'], 'sw1_reset'))
                            cocotb.start_soon(self.process_start())
                    elif address > RGU_REG_TIMER1_ADDR and previous_value != new_value and self.reset_flag != True:
                        self.sample_scoreboard(76)
                        cocotb.start_soon(self.transaction_waiting(previous_value, new_value[::-1], address))
                    elif address > RGU_REG_TIMER1_ADDR and previous_value != new_value and self.reset_flag == True:
                        self.sample_scoreboard(77)

                        if self.model.addresses[address][2] == 1:
                            self.sample_scoreboard(78)

                            if previous_value > new_value:
                                self.sample_scoreboard(79)
                                self.assert_counter = self.assert_counter + 1 if address != RGU_REG_SYS_SWRST_ADDR else self.assert_counter + 13 # When changing RGU_REG_SYS_SWRST, it is expected to receive 13 response signals
                            elif previous_value < new_value:
                                self.sample_scoreboard(80)
                                self.assert_counter = self.assert_counter - 1 if address != RGU_REG_SYS_SWRST_ADDR else self.assert_counter - 13 # When changing RGU_REG_SYS_SWRST, it is expected to receive 13 response signals
                        else:
                            self.sample_scoreboard(81)
                            counter = 0

                            for symbol in previous_value[::-1]:
                                if symbol > new_value[counter]:
                                    self.sample_scoreboard(82)
                                    self.assert_counter += 1
                                elif symbol < new_value[counter]:
                                    self.sample_scoreboard(83)
                                    self.assert_counter -= 1

                                counter += 1

                elif apb_dut_trn.direction == apb_direction.READ:
                    self.sample_scoreboard(84)
                    self.expected_value = getattr(self.model, self.model.addresses[address][0])

                    if int(apb_dut_trn.data) != self.expected_value:
                        self.is_error(f"Expected value = {self.expected_value}. Received value = {int(apb_dut_trn.data)}. Reading APB-transaction {apb_dut_trn}")
    
    async def create_rst_dut_trn(self):
        """Creating tracking coroutines for each reset channel"""
        for key in reset_agent_names.keys():
            cocotb.start_soon(self.get_rst_dut_trn(key))

    async def run_phase(self):
        """Start of scoreboard operation""" 
        self.model = rgu_model()

        if self.model.rgu_reg_timer0 > RGU_TIM_MAX or self.model.rgu_reg_timer0 < RGU_TIM_MIN or self.model.rgu_reg_timer1 > RGU_TIM_MAX or self.model.rgu_reg_timer1 < RGU_TIM_MIN:
            raise RuntimeError(f"Incorrect values for timers")

        cocotb.start_soon(self.get_apb_dut_trn())
        cocotb.start_soon(self.create_rst_dut_trn())

    def check_queue(self, name, checked_queue, flag):
        """Checking the queue for emptiness"""
        if not checked_queue.empty():
            mistake_massiv = []

            while not checked_queue.empty():
                mistake_transaction = checked_queue.get_nowait()

                if flag:
                    mistake_massiv.append(mistake_transaction[1])
                elif mistake_transaction[0] != 'apb_rst':
                    mistake_massiv.append((mistake_transaction[0], mistake_transaction[1].rst_st, mistake_transaction[1].time_assert))
            
            if len(mistake_massiv) != 0:
                self.is_error(f"Unprocessed transactions in {name}: {mistake_massiv}")

    def extract_phase(self):
        """Verify that there are no unprocessed transactions, pending coroutines, or errors in the simulation process"""
        self.check_queue("proirity_queue", self.priority_queue, True)
        self.check_queue("reset_queue", self.reset_queue, False)
        self.check_queue("registers_queue", self.registers_queue, False)

        for key in self.priority_map:
            if not key.startswith('sw'):
                self.check_queue(f"{key}_deassert_queue", getattr(self, f"{key}_deassert_queue"), False)

        if self.reset_count != 0:
            self.is_error(f"For {self.reset_count} signals there was no response from RGU")
        
        if self.apb_count != 0:
            self.is_error(f"For {self.apb_count} APB transactions there was no response from RGU")

        if (self.error_count > 0):
            raise RuntimeError(f"There are mistakes. Check them")
    
    @CoverPoint("rgu_top.scoreboard_checker", bins = list(range(85)))
    def sample_scoreboard(self, value):
        pass
