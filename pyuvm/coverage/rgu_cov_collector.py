from rgu_pkg import *

class rgu_cov_collector(uvm_component):
    class uvm_AnalysisImp(uvm_analysis_export):
        def __init__(self, name, parent, write_fn):
            super().__init__(name, parent)
            self.write_fn = write_fn

        def write(self, tt):
            self.write_fn(tt)

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.model_for_coverage = rgu_model()

        for value in self.model_for_coverage.addresses.values():
            if value[0] not in ['rgu_reg_timer0', 'rgu_reg_timer1', 'rgu_reg_rst_status']:
                if value[2] == 1:
                    setattr(self, f"{value[0]}_previous_value", getattr(self.model_for_coverage, value[0]))
                    self.start_registers_coverage(value[0], None, do_samplying = False)
                else:
                    value_from_model = getattr(self.model_for_coverage, value[0])

                    for number in range(value[2]):
                        setattr(self, f"{value[0]}_{value[2] - number - 1}_previous_value", int(bin(value_from_model)[2:].zfill(value[2])[number]))
                        self.start_registers_coverage(f"{value[0]}_{value[2] - number - 1}", None, do_samplying = False)

        for key in reset_agent_names.keys():
            self.create_reset_function(f"{key}_cov")

        for key in reset_agent_names.keys():
            setattr(self, f"analysis_export_{key}", self.uvm_AnalysisImp(f"analysis_export_{key}_rst", self, getattr(self, f"{key}_cov")))
        
        self.analysis_export_apb = self.uvm_AnalysisImp("analysis_export_apb", self, self.write_apb_cov)
 
    def create_reset_function(self, key):
        def function(rst_item):
            self.start_reset_coverage(key, rst_item.rst_st.name, do_samplying = True)

        setattr(self, key, function)
        self.start_reset_coverage(key, None, do_samplying = False)
    
    def comparison(self, naming, first_value, second_value):
        if first_value < second_value:
            self.start_registers_coverage(naming, 0, True)
        elif first_value > second_value:
            self.start_registers_coverage(naming, 1, True)

    def write_apb_cov(self, apb_item):
        address_number = bin(int(apb_item.address, 16))[2:-2] + '00'

        if int(address_number, 2) > 0xf00:
            address_number = int(address_number[-12:], 2)
        else:
            address_number = int(address_number, 2)
        
        naming = 'RESERVED' if address_number > RGU_REG_CPU_PWRUP_HEAVY_SWRST_ADDR else self.model_for_coverage.addresses[address_number][0]
        self.sample_apb_trn(naming, apb_item.direction)

        if naming != 'RESERVED' and (address_number < RGU_REG_RST_STATUS_ADDR or address_number > RGU_REG_TIMER1_ADDR):
            count = self.model_for_coverage.addresses[address_number][2]

            if count == 1:
                self.comparison(naming, int(apb_item.data[-1]), getattr(self, f"{naming}_previous_value"))
                setattr(self, f"{naming}_previous_value", int(apb_item.data[-1]))
            else:
                for number in range(count):
                    self.comparison(f"{naming}_{count - number - 1}", int(bin(apb_item.data)[2:].zfill(count)[number]), getattr(self, f"{naming}_{count - number - 1}_previous_value"))
                    setattr(self, f"{naming}_{count - number - 1}_previous_value", int(bin(apb_item.data)[2:].zfill(count)[number]))

    def start_reset_coverage(self, key, value, do_samplying):
        @CoverPoint(f"rgu_top.resets.{key[:-4]}_reset_dut", bins = [rst_state.RST_ASSERT.name, rst_state.RST_DEASSERT.name])
        def sample_rst_dut(value):
            pass
        
        if do_samplying:
            sample_rst_dut(value)
    
    @CoverPoint("rgu_top.apb.register_name", xf = lambda x, y: x, bins = ['rgu_reg_glb', 'rgu_reg_rst_status', 'rgu_reg_timer0', 'rgu_reg_timer1', 'rgu_reg_sb_swrst', 'rgu_reg_sys_swrst', 'rgu_reg_sram_swrst', \
        'rgu_reg_ddr_swrst', 'rgu_reg_usb_swrst', 'rgu_reg_mmc_swrst', 'rgu_reg_dmac_swrst', 'rgu_reg_qspi_swrst', 'rgu_reg_spi_swrst', 'rgu_reg_i2c_swrst', 'rgu_reg_uart_swrst', 'rgu_reg_gpio_swrst', 'rgu_reg_i2s_swrst', 'rgu_reg_gpu_swrst', \
        'rgu_reg_videc_swrst', 'rgu_reg_vicod_swrst', 'rgu_reg_camera_swrst', 'rgu_reg_display_swrst', 'rgu_reg_llc_swrst', 'rgu_reg_cpu_swrst', 'rgu_reg_pwm_swrst', 'rgu_reg_cpu_pwrup_swrst', 'rgu_reg_cpu_pwrup_heavy_swrst', 'RESERVED'])
    @CoverPoint("rgu_top.apb.direction", xf = lambda x, y: y, bins = [0, 1], bins_labels = ["READ", "WRITE"])
    @CoverCross(name = "rgu_top.apb.register_name_direction", items = ["rgu_top.apb.register_name", "rgu_top.apb.direction"])
    def sample_apb_trn(self, register_name, direction):
        pass
    
    def start_registers_coverage(self, key, value, do_samplying):
        @CoverPoint(f"rgu_top.apb.transitions.{key}", bins = [0, 1], bins_labels = ["1 => 0", "0 => 1"])
        def sample_transitions(value):
            pass
        
        if do_samplying:
            sample_transitions(value)
    
    async def run_phase(self):
        while True:
            await cocotb.triggers.Timer(100, "ns")

    def coverage_report(self, xml_flag, yml_flag):
        coverage_db.report_coverage(self.logger.info, bins=True)

        if xml_flag:
            coverage_db.export_to_xml(filename="current_coverage.xml")
            merge_coverage(self.logger.info, 'coverage.xml', 'current_coverage.xml', 'coverage.xml')
        else:
            coverage_db.export_to_xml(filename="coverage.xml")
        
        if yml_flag:
            coverage_db.export_to_yaml(filename="current_coverage.yml")
            merge_coverage(self.logger.info, 'coverage.yml', 'current_coverage.yml', 'coverage.yml')
        else:
            coverage_db.export_to_yaml(filename="coverage.yml")
        
    def final_phase(self):
        my_path = str(Path().resolve())
        xml_file_path = Path(my_path + '/coverage.xml')
        yml_file_path = Path(my_path + '/coverage.yml')
        self.coverage_report(xml_file_path.is_file(), yml_file_path.is_file())
