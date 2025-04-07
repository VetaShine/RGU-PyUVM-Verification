from rgu_pkg import *


class rgu_base_test(uvm_test):
    """
    Base test for the module
    """

    def __init__(self, name, parent):
        super().__init__(name, parent)

    def build_phase(self):
        self.env = rgu_env("rgu_env", self)
        self.cfg = rgu_env_cfg("rgu_env_cfg")
        self.cfg.build()
        ConfigDB().set(self, "rgu_env", "rgu_env_cfg", self.cfg)

        root_logger = logging.getLogger()
        file_handler = FileHandler("cocotb.log", mode="w")
        file_handler.setFormatter(SimLogFormatter())
        root_logger.addHandler(file_handler)

    def start_clock(self, name, frequency):
        sig = getattr(cocotb.top, name)
        clock = cocotb.clock.Clock(sig, frequency, units="ns")
        cocotb.start_soon(clock.start(start_high=False))

    def end_of_elaboration_phase(self):
        try:
            self.set_logging_level_hier(cocotb.plusargs["loglvl"])
        except KeyError:
            self.set_logging_level_hier(INFO)
            
    async def run_phase(self):
        pass

    async def run(self):
        raise NotImplementedError()
