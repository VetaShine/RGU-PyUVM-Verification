from rgu_pkg import *


RGU_REG_GLB_ADDR = 0x0
RGU_REG_RST_STATUS_ADDR = 0x4
RGU_REG_TIMER0_ADDR = 0x8
RGU_REG_TIMER1_ADDR = 0xc
RGU_REG_SB_SWRST_ADDR = 0x10
RGU_REG_SYS_SWRST_ADDR = 0x14
RGU_REG_SRAM_SWRST_ADDR = 0x18
RGU_REG_DDR_SWRST_ADDR = 0x1c
RGU_REG_USB_SWRST_ADDR = 0x20
RGU_REG_MMC_SWRST_ADDR = 0x24
RGU_REG_DMAC_SWRST_ADDR = 0x28
RGU_REG_QSPI_SWRST_ADDR = 0x2c
RGU_REG_SPI_SWRST_ADDR = 0x30
RGU_REG_I2C_SWRST_ADDR = 0x34
RGU_REG_UART_SWRST_ADDR = 0x38
RGU_REG_GPIO_SWRST_ADDR = 0x3c
RGU_REG_I2S_SWRST_ADDR = 0x40
RGU_REG_GPU_SWRST_ADDR = 0x44
RGU_REG_VIDEC_SWRST_ADDR = 0x48
RGU_REG_VICOD_SWRST_ADDR = 0x4c
RGU_REG_CAMERA_SWRST_ADDR = 0x50
RGU_REG_DISPLAY_SWRST_ADDR = 0x54
RGU_REG_LLC_SWRST_ADDR = 0x58
RGU_REG_CPU_SWRST_ADDR = 0x5c
RGU_REG_PWM_SWRST_ADDR = 0x60
RGU_REG_CPU_PWRUP_SWRST_ADDR = 0x64
RGU_REG_CPU_PWRUP_HEAVY_SWRST_ADDR = 0x68

RGU_RST_STATUS_PWRGD = 0x1
RGU_RST_STATUS_SYS_RESET = 0x2
RGU_RST_STATUS_SB_WDT_RESET = 0x4
RGU_RST_STATUS_SYS_WDT_RESET = 0x8
RGU_RST_STATUS_SW0_RESET = 0x10
RGU_RST_STATUS_SW1_RESET = 0x20

RGU_TIM0 = cocotb.top.TIM0.value
RGU_TIM1 = cocotb.top.TIM1.value
RGU_TIM_MAX = 0xffffffff
RGU_TIM_MIN = 0x1
COMFORT_LIMIT_TIM_MAX = 0x500
COMFORT_LIMIT_TIM_MIN = 0x24

RESET_DURATION_LIMIT_MIN = 0x5
RESET_COMFORT_DURATION_LIMIT = 0x1e
WDT_EXACT_DURATION_LIMIT = 3
WDT_RESET_PERMISSION = 0x3c
WDT_RESET_PROHIBITION = 0x0
CLASSIC_DEASSERT_COUNT = 10
APB_CAPACITY = 32

SIMULTANEOUS_RESETS_DURATION_LIMIT_MIN = 0x1e
SIMULTANEOUS_RESETS_DURATION_LIMIT_MAX = 0x32
SIMULTANEOUS_SW_RESETS = 0x3
SIMULTANEOUS_MIN_COUNT = 2
SIMULTANEOUS_MAX_COUNT = 7
MIN_CYCLES_COUNT_AFTER_GLB = 1
MAX_CYCLES_COUNT_AFTER_GLB = 10
PCLK_FAILURE_TIME_LIMIT = 1000

APB_DELAY = 30
RESET_DELAY = 5
SHORT_WAITING_DELAY = 3
SYS_RESET_N_DELAY = 2
SYS_PWRGD_DELAY = 3
WDT_DELAY = 5
ASSERT_DELAY = 5



class rgu_model:
    """Register model RGU"""
    def __init__(self):
        # Values in registers on reset
        self.rgu_reg_glb = 0x0
        self.rgu_reg_rst_status = 0x1
        self.rgu_reg_timer0 = RGU_TIM0 
        self.rgu_reg_timer1 = RGU_TIM1
        self.rgu_reg_sb_swrst = 0x0
        self.rgu_reg_sys_swrst = 0x1
        self.rgu_reg_sram_swrst = 0x1
        self.rgu_reg_ddr_swrst = 0x1
        self.rgu_reg_usb_swrst = 0xf
        self.rgu_reg_mmc_swrst = 0xf
        self.rgu_reg_dmac_swrst = 0x1
        self.rgu_reg_qspi_swrst = 0x3
        self.rgu_reg_spi_swrst = 0x3f
        self.rgu_reg_i2c_swrst = 0x7f
        self.rgu_reg_uart_swrst = 0x1f
        self.rgu_reg_gpio_swrst = 0x3
        self.rgu_reg_i2s_swrst = 0x1f
        self.rgu_reg_gpu_swrst = 0x1
        self.rgu_reg_videc_swrst = 0x1
        self.rgu_reg_vicod_swrst = 0x1
        self.rgu_reg_camera_swrst = 0x1
        self.rgu_reg_display_swrst = 0x3
        self.rgu_reg_llc_swrst = 0x1
        self.rgu_reg_cpu_swrst = 0xff
        self.rgu_reg_pwm_swrst = 0x7
        self.rgu_reg_cpu_pwrup_swrst = 0x1
        self.rgu_reg_cpu_pwrup_heavy_swrst = 0x1

        self.addresses = {
            # address: [register name, access, digit capacity]
            RGU_REG_GLB_ADDR : ['rgu_reg_glb', 'rw', 6],
            RGU_REG_RST_STATUS_ADDR : ['rgu_reg_rst_status', 'r', 6],
            RGU_REG_TIMER0_ADDR : ['rgu_reg_timer0', 'rw', 32],
            RGU_REG_TIMER1_ADDR : ['rgu_reg_timer1', 'rw', 32],
            RGU_REG_SB_SWRST_ADDR : ['rgu_reg_sb_swrst', 'rw', 7],
            RGU_REG_SYS_SWRST_ADDR : ['rgu_reg_sys_swrst', 'rw', 1],
            RGU_REG_SRAM_SWRST_ADDR : ['rgu_reg_sram_swrst', 'rw', 1],
            RGU_REG_DDR_SWRST_ADDR : ['rgu_reg_ddr_swrst', 'rw', 1],
            RGU_REG_USB_SWRST_ADDR : ['rgu_reg_usb_swrst', 'rw', 4],
            RGU_REG_MMC_SWRST_ADDR : ['rgu_reg_mmc_swrst', 'rw', 4],
            RGU_REG_DMAC_SWRST_ADDR : ['rgu_reg_dmac_swrst', 'rw', 1],
            RGU_REG_QSPI_SWRST_ADDR : ['rgu_reg_qspi_swrst', 'rw', 2],
            RGU_REG_SPI_SWRST_ADDR : ['rgu_reg_spi_swrst', 'rw', 6],
            RGU_REG_I2C_SWRST_ADDR : ['rgu_reg_i2c_swrst', 'rw', 7],
            RGU_REG_UART_SWRST_ADDR : ['rgu_reg_uart_swrst', 'rw', 5],
            RGU_REG_GPIO_SWRST_ADDR : ['rgu_reg_gpio_swrst', 'rw', 2],
            RGU_REG_I2S_SWRST_ADDR : ['rgu_reg_i2s_swrst', 'rw', 5],
            RGU_REG_GPU_SWRST_ADDR : ['rgu_reg_gpu_swrst', 'rw', 1],
            RGU_REG_VIDEC_SWRST_ADDR : ['rgu_reg_videc_swrst', 'rw', 1],
            RGU_REG_VICOD_SWRST_ADDR : ['rgu_reg_vicod_swrst', 'rw', 1],
            RGU_REG_CAMERA_SWRST_ADDR : ['rgu_reg_camera_swrst', 'rw', 1],
            RGU_REG_DISPLAY_SWRST_ADDR : ['rgu_reg_display_swrst', 'rw', 2],
            RGU_REG_LLC_SWRST_ADDR : ['rgu_reg_llc_swrst', 'rw', 1],
            RGU_REG_CPU_SWRST_ADDR : ['rgu_reg_cpu_swrst', 'rw', 8],
            RGU_REG_PWM_SWRST_ADDR : ['rgu_reg_pwm_swrst', 'rw', 3],
            RGU_REG_CPU_PWRUP_SWRST_ADDR : ['rgu_reg_cpu_pwrup_swrst', 'rw', 1],
            RGU_REG_CPU_PWRUP_HEAVY_SWRST_ADDR : ['rgu_reg_cpu_pwrup_heavy_swrst', 'rw', 1]
        }
