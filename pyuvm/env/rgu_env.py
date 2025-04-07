from rgu_pkg import *


class rgu_env (uvm_env):
    """Instantiate components"""
    def build_phase(self):
        self.rgu_env_cfg = ConfigDB().get(self, "", "rgu_env_cfg")
        
        if (self.rgu_env_cfg.has_scoreboard):
            self.scoreboard = rgu_scoreboard.create("rgu_scoreboard", self)
            self.scoreboard.set_rgu_env_cfg(self.rgu_env_cfg)
        
        if (self.rgu_env_cfg.has_cov):
            self.cov_collector = rgu_cov_collector.create("rgu_cov_collector", self)

        for key, value in reset_agent_names.items():
            setattr(self, f'{key}_agent', reset_agent.create(f"{key}_agent", self))

            if value == 1:
                ConfigDB().set(self, f"{key}_agent", "cfg", self.rgu_env_cfg.active_reset_agent_cfg)
            else:
                ConfigDB().set(self, f"{key}_agent", "cfg", self.rgu_env_cfg.passive_reset_agent_cfg)
        
        if (self.rgu_env_cfg.has_apb_agent):
            self.apb_agent = apb_master_agent.create("apb_agent", self)
            ConfigDB().set(self, "apb_agent", "cfg", self.rgu_env_cfg.apb_agent_cfg)


    def connect_phase(self):
        if (self.rgu_env_cfg.has_scoreboard):
            for key, value in reset_agent_names.items():
                (getattr(self, f'{key}_agent')).monitor.ap.connect((getattr(self.scoreboard, f'{key}_fifo_reset')).analysis_export)
            
            if (self.rgu_env_cfg.has_apb_agent):
                self.apb_agent.monitor.ap.connect(self.scoreboard.apb_fifo_trans.analysis_export)

        if (self.rgu_env_cfg.has_cov):
            for key, value in reset_agent_names.items():
                (getattr(self, f'{key}_agent')).monitor.ap.connect(getattr(self.cov_collector, f'analysis_export_{key}'))
            
            if (self.rgu_env_cfg.has_apb_agent):
                self.apb_agent.monitor.ap.connect(self.cov_collector.analysis_export_apb)
