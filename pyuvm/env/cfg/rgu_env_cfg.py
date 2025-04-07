from rgu_pkg import *

class rgu_env_cfg (uvm_object):
    def __init__(self, name):
        super().__init__(name)
        self.has_scoreboard = 1
        self.has_apb_agent = 1
        self.is_active = 1
        self.clock_period = 41.6
        self.pclock_period = 15

        try:
            self.has_cov = cocotb.plusargs["en_cov"]
        except KeyError:
            self.has_cov = False
            

    def build(self):
        self.build_active_reset_agent_cfg()
        self.build_passive_reset_agent_cfg()

        if (self.has_apb_agent):
            self.build_apb_agent()


    def build_active_reset_agent_cfg(self):
        self.active_reset_agent_cfg = reset_agent_cfg("active_reset_agent_cfg")
        self.active_reset_agent_cfg.active_level = reset_level.LOW_LEVEL
        self.active_reset_agent_cfg.is_active = self.is_active


    def build_passive_reset_agent_cfg(self):
        self.passive_reset_agent_cfg = reset_agent_cfg("passive_reset_agent_cfg")
        self.passive_reset_agent_cfg.active_level = reset_level.LOW_LEVEL
        self.passive_reset_agent_cfg.is_active = 0


    def build_apb_agent(self):
        self.apb_agent_cfg = apb_master_agent_cfg("apb_agent_cfg")
        self.apb_agent_cfg.fix_pready_timeout = 50
        self.apb_agent_cfg.is_active = self.is_active
