`ifndef INC_RGU_WRAPPER
`define INC_RGU_WRAPPER

module rgu_top_wrapper
#(
    parameter
    TIM0 = `RGU_TIM0,
    TIM1 = `RGU_TIM1
)();


	// Number of WDT timers
	localparam WDT_NUM = 4;
	// Number of GPTs
	localparam GPT_NUM  = 8;
	// Number of SRAMs
	localparam SRAM_NUM = 1;
	// Number of USB controllers
	localparam USB_NUM = 4;
	// Number of *MMC controllers
	localparam MMC_NUM = 4;
	// Number of QSPI controllers
	localparam QSPI_NUM = 2;
	// Number of SPI controllers
	localparam SPI_NUM  = 6;
	// Number of I2C controllers
	localparam I2C_NUM  = 7;
	// Number of UART controllers
	localparam UART_NUM = 5;
	// Number of GPIO controllers
	localparam GPIO_NUM = 2;
	// Number of I2S controllers
	localparam I2S_NUM = 5;
	// Number of CPU cores
	localparam CPU_NUM = 8;
	// Number of I2C cores in SB
	localparam SB_I2C_NUM = 2;
	// Number of PWMs
	localparam PWM_NUM = 3;
	// Number of DISPLAYs
	localparam DISP_NUM = 2;

    wire             cocotb_clock       ;
    wire             cocotb_pclock       ;

    // APB master
    wire [`RGU_ADDR_WIDTH   -1:0] apb_vip_m0_paddr   ; 
    wire [3    -1:0] apb_vip_m0_pprot   ; 
    wire             apb_vip_m0_psel    ; 
    wire             apb_vip_m0_penable ; 
    wire             apb_vip_m0_pwrite  ; 
    wire [`RGU_DATA_WIDTH   -1:0] apb_vip_m0_pwdata  ; 
    wire [`RGU_DATA_WIDTH/8 -1:0] apb_vip_m0_pstrb   ; 
    wire             apb_vip_m0_pready  ; 
    wire [`RGU_DATA_WIDTH   -1:0] apb_vip_m0_prdata  ; 
    wire             apb_vip_m0_pslverr ;
    wire             apb_vip_m0_pclk    ;
    wire             apb_vip_m0_presetn ;

    // Active RST-masters

    //RST VIP master[0] wires
    wire             rst_vip_m0_clk;
    wire             rst_vip_m0_reset;

    //RST VIP master[1] wires
    wire             rst_vip_m1_clk;
    wire             rst_vip_m1_reset;

    //RST VIP master[2] wires
    wire             rst_vip_m2_clk;
    wire             rst_vip_m2_reset;

    //RST VIP master[3] wires
    wire             rst_vip_m3_clk;
    logic             rst_vip_m3_reset;

    //RST VIP master[4] wires
    wire             rst_vip_m4_clk;
    logic             rst_vip_m4_reset;

    //RST VIP master[5] wires
    wire             rst_vip_m5_clk;
    logic              rst_vip_m5_reset;

    //RST VIP master[6] wires
    wire             rst_vip_m6_clk;
    logic             rst_vip_m6_reset;

    //RST VIP master[7] wires
    wire             rst_vip_m7_clk;
    wire             rst_vip_m7_reset;

    // Passive RST-masters

    //RST VIP master[8] wires
    wire             rst_vip_m8_clk;
    wire             rst_vip_m8_reset;

    //RST VIP master[9] wires
    wire             rst_vip_m9_clk;
    wire             rst_vip_m9_reset;

    //RST VIP master[10] wires
    wire             rst_vip_m10_clk;
    wire             rst_vip_m10_reset;

    //RST VIP master[11] wires
    wire             rst_vip_m11_clk;
    wire             rst_vip_m11_reset;

    //RST VIP master[12] wires
    wire             rst_vip_m12_clk;
    wire             rst_vip_m12_reset;

    //RST VIP master[13] wires
    wire             rst_vip_m13_clk;
    wire             rst_vip_m13_reset;

    //RST VIP master[14] wires
    wire             rst_vip_m14_clk;
    wire             rst_vip_m14_reset;

    //RST VIP master[15] wires
    wire             rst_vip_m15_clk;
    wire             rst_vip_m15_reset;

    //RST VIP master[16] wires
    wire             rst_vip_m16_clk;
    wire             rst_vip_m16_reset;

    //RST VIP master[17] wires
    wire             rst_vip_m17_clk;
    wire             rst_vip_m17_reset;

    //RST VIP master[18] wires
    wire             rst_vip_m18_clk;
    wire             rst_vip_m18_reset;

    //RST VIP master[19] wires
    wire             rst_vip_m19_clk;
    wire             rst_vip_m19_reset;

    //RST VIP master[20] wires
    wire             rst_vip_m20_clk;
    wire             rst_vip_m20_reset;

    //RST VIP master[21] wires
    wire             rst_vip_m21_clk;
    wire             rst_vip_m21_reset;

    //RST VIP master[22] wires
    wire             rst_vip_m22_clk;
    wire             rst_vip_m22_reset;

    //RST VIP master[23] wires
    wire             rst_vip_m23_clk;
    wire             rst_vip_m23_reset;

    //RST VIP master[24] wires
    wire             rst_vip_m24_clk;
    wire             rst_vip_m24_reset;

    //RST VIP master[25] wires
    wire             rst_vip_m25_clk;
    wire             rst_vip_m25_reset;

    //RST VIP master[26] wires
    wire             rst_vip_m26_clk;
    wire             rst_vip_m26_reset;

    //RST VIP master[27] wires
    wire             rst_vip_m27_clk;
    wire             rst_vip_m27_reset;

    //RST VIP master[28] wires
    wire             rst_vip_m28_clk;
    wire             rst_vip_m28_reset;

    //RST VIP master[29] wires
    wire             rst_vip_m29_clk;
    wire             rst_vip_m29_reset;

    //RST VIP master[30] wires
    wire             rst_vip_m30_clk;
    wire             rst_vip_m30_reset;

    //RST VIP master[31] wires
    wire             rst_vip_m31_clk;
    wire             rst_vip_m31_reset;

    //RST VIP master[32] wires
    wire             rst_vip_m32_clk;
    wire             rst_vip_m32_reset;

    //RST VIP master[33] wires
    wire             rst_vip_m33_clk;
    wire             rst_vip_m33_reset;

    //RST VIP master[34] wires
    wire             rst_vip_m34_clk;
    wire             rst_vip_m34_reset;

    //RST VIP master[35] wires
    wire             rst_vip_m35_clk;
    wire             rst_vip_m35_reset;

    //RST VIP master[36] wires
    wire             rst_vip_m36_clk;
    wire             rst_vip_m36_reset;

    //RST VIP master[37] wires
    wire             rst_vip_m37_clk;
    wire             rst_vip_m37_reset;

    //RST VIP master[38] wires
    wire             rst_vip_m38_clk;
    wire             rst_vip_m38_reset;

    //RST VIP master[39] wires
    wire             rst_vip_m39_clk;
    wire             rst_vip_m39_reset;

    //RST VIP master[40] wires
    wire             rst_vip_m40_clk;
    wire             rst_vip_m40_reset;

    //RST VIP master[41] wires
    wire             rst_vip_m41_clk;
    wire             rst_vip_m41_reset;

    //RST VIP master[42] wires
    wire             rst_vip_m42_clk;
    wire             rst_vip_m42_reset;

    //RST VIP master[43] wires
    wire             rst_vip_m43_clk;
    wire             rst_vip_m43_reset;

    //RST VIP master[44] wires
    wire             rst_vip_m44_clk;
    wire             rst_vip_m44_reset;

    //RST VIP master[45] wires
    wire             rst_vip_m45_clk;
    wire             rst_vip_m45_reset;

    //RST VIP master[46] wires
    wire             rst_vip_m46_clk;
    wire             rst_vip_m46_reset;

    //RST VIP master[47] wires
    wire             rst_vip_m47_clk;
    wire             rst_vip_m47_reset;

    //RST VIP master[48] wires
    wire             rst_vip_m48_clk;
    wire             rst_vip_m48_reset;

    //RST VIP master[49] wires
    wire             rst_vip_m49_clk;
    wire             rst_vip_m49_reset;

    //RST VIP master[50] wires
    wire             rst_vip_m50_clk;
    wire             rst_vip_m50_reset;

    //RST VIP master[51] wires
    wire             rst_vip_m51_clk;
    wire             rst_vip_m51_reset;

    //RST VIP master[52] wires
    wire             rst_vip_m52_clk;
    wire             rst_vip_m52_reset;

    //RST VIP master[53] wires
    wire             rst_vip_m53_clk;
    wire             rst_vip_m53_reset;

    //RST VIP master[54] wires
    wire             rst_vip_m54_clk;
    wire             rst_vip_m54_reset;

    //RST VIP master[55] wires
    wire             rst_vip_m55_clk;
    wire             rst_vip_m55_reset;

    //RST VIP master[56] wires
    wire             rst_vip_m56_clk;
    wire             rst_vip_m56_reset;

    //RST VIP master[57] wires
    wire             rst_vip_m57_clk;
    wire             rst_vip_m57_reset;

    //RST VIP master[58] wires
    wire             rst_vip_m58_clk;
    wire             rst_vip_m58_reset;

    //RST VIP master[59] wires
    wire             rst_vip_m59_clk;
    wire             rst_vip_m59_reset;

    //RST VIP master[60] wires
    wire             rst_vip_m60_clk;
    wire             rst_vip_m60_reset;

    //RST VIP master[61] wires
    wire             rst_vip_m61_clk;
    wire             rst_vip_m61_reset;

    //RST VIP master[62] wires
    wire             rst_vip_m62_clk;
    wire             rst_vip_m62_reset;

    //RST VIP master[63] wires
    wire             rst_vip_m63_clk;
    wire             rst_vip_m63_reset;

    //RST VIP master[64] wires
    wire             rst_vip_m64_clk;
    wire             rst_vip_m64_reset;

    //RST VIP master[65] wires
    wire             rst_vip_m65_clk;
    wire             rst_vip_m65_reset;

    //RST VIP master[66] wires
    wire             rst_vip_m66_clk;
    wire             rst_vip_m66_reset;

    //RST VIP master[67] wires
    wire             rst_vip_m67_clk;
    wire             rst_vip_m67_reset;

    //RST VIP master[68] wires
    wire             rst_vip_m68_clk;
    wire             rst_vip_m68_reset;

    //RST VIP master[69] wires
    wire             rst_vip_m69_clk;
    wire             rst_vip_m69_reset;

    //RST VIP master[70] wires
    wire             rst_vip_m70_clk;
    wire             rst_vip_m70_reset;

    //RST VIP master[71] wires
    wire             rst_vip_m71_clk;
    wire             rst_vip_m71_reset;

    //RST VIP master[72] wires
    wire             rst_vip_m72_clk;
    wire             rst_vip_m72_reset;

    //RST VIP master[73] wires
    wire             rst_vip_m73_clk;
    wire             rst_vip_m73_reset;

    //RST VIP master[74] wires
    wire             rst_vip_m74_clk;
    wire             rst_vip_m74_reset;

    //RST VIP master[75] wires
    wire             rst_vip_m75_clk;
    wire             rst_vip_m75_reset;

    //RST VIP master[76] wires
    wire             rst_vip_m76_clk;
    wire             rst_vip_m76_reset;

    //RST VIP master[77] wires
    wire             rst_vip_m77_clk;
    wire             rst_vip_m77_reset;

    //RST VIP master[78] wires
    wire             rst_vip_m78_clk;
    wire             rst_vip_m78_reset;

    //RST VIP master[79] wires
    wire             rst_vip_m79_clk;
    wire             rst_vip_m79_reset;

    //RST VIP master[80] wires
    wire             rst_vip_m80_clk;
    wire             rst_vip_m80_reset;

    //RST VIP master[81] wires
    wire             rst_vip_m81_clk;
    wire             rst_vip_m81_reset;

    //RST VIP master[82] wires
    wire             rst_vip_m82_clk;
    wire             rst_vip_m82_reset;

    //RST VIP master[83] wires
    wire             rst_vip_m83_clk;
    wire             rst_vip_m83_reset;

    //RST VIP master[84] wires
    wire             rst_vip_m84_clk;
    wire             rst_vip_m84_reset;

    //RST VIP master[85] wires
    wire             rst_vip_m85_clk;
    wire             rst_vip_m85_reset;

    //RST VIP master[86] wires
    wire             rst_vip_m86_clk;
    wire             rst_vip_m86_reset;

    //RST VIP master[87] wires
    wire             rst_vip_m87_clk;
    wire             rst_vip_m87_reset;

    //RST VIP master[88] wires
    wire             rst_vip_m88_clk;
    wire             rst_vip_m88_reset;

    logic  wdt_rst_n [WDT_NUM];
    logic  wdt_rst_n_layer [WDT_NUM];
    wire rst_sb_i2c_n[SB_I2C_NUM];
    wire rst_wdt_n[WDT_NUM];
    wire rst_gpt_n[GPT_NUM];
    wire rst_sram_n[SRAM_NUM];
    wire rst_usb_n[USB_NUM];
    wire rst_mmc_n[MMC_NUM];
    wire rst_qspi_n[QSPI_NUM];
    wire rst_spi_n[SPI_NUM];
    wire rst_i2c_n[I2C_NUM];
    wire rst_uart_n[UART_NUM];
    wire rst_gpio_n[GPIO_NUM];
    wire rst_pwm_n[PWM_NUM];
    wire rst_i2s_n[I2S_NUM];
    wire rst_display_n[DISP_NUM];
    wire rst_cpu_n[CPU_NUM];

    // Active RST-masters

    // clk connect to RST-master[0] VIP
    assign rst_vip_m0_clk = cocotb_clock;

    // clk connect to RST-master[1] VIP
    assign rst_vip_m1_clk = cocotb_clock;

    // clk connect to RST-master[2] VIP
    assign rst_vip_m2_clk = cocotb_clock;

    // clk connect to RST-master[3] VIP
    assign rst_vip_m3_clk = cocotb_clock;

    // clk connect to RST-master[4] VIP
    assign rst_vip_m4_clk = cocotb_clock;

    // clk connect to RST-master[5] VIP
    assign rst_vip_m5_clk = cocotb_clock;

    // clk connect to RST-master[6] VIP
    assign rst_vip_m6_clk = cocotb_clock;

    // clk connect to RST-master[7] VIP
    assign rst_vip_m7_clk = cocotb_clock;

    // Passive RST-masters

    // clk connect to RST-master[8] VIP
    assign rst_vip_m8_clk = cocotb_clock;

    // clk connect to RST-master[9] VIP
    assign rst_vip_m9_clk = cocotb_clock;

    // clk connect to RST-master[10] VIP
    assign rst_vip_m10_clk = cocotb_clock;

    // clk connect to RST-master[11] VIP
    assign rst_vip_m11_clk = cocotb_clock;

    // clk connect to RST-master[12] VIP
    assign rst_vip_m12_clk = cocotb_clock;

    // clk connect to RST-master[13] VIP
    assign rst_vip_m13_clk = cocotb_clock;

    // clk connect to RST-master[14] VIP
    assign rst_vip_m14_clk = cocotb_clock;

    // clk connect to RST-master[15] VIP
    assign rst_vip_m15_clk = cocotb_clock;

    // clk connect to RST-master[16] VIP
    assign rst_vip_m16_clk = cocotb_clock;

    // clk connect to RST-master[17] VIP
    assign rst_vip_m17_clk = cocotb_clock;

    // clk connect to RST-master[18] VIP
    assign rst_vip_m18_clk = cocotb_clock;

    // clk connect to RST-master[19] VIP
    assign rst_vip_m19_clk = cocotb_clock;

    // clk connect to RST-master[20] VIP
    assign rst_vip_m20_clk = cocotb_clock;

    // clk connect to RST-master[21] VIP
    assign rst_vip_m21_clk = cocotb_clock;

    // clk connect to RST-master[22] VIP
    assign rst_vip_m22_clk = cocotb_clock;

    // clk connect to RST-master[23] VIP
    assign rst_vip_m23_clk = cocotb_clock;

    // clk connect to RST-master[24] VIP
    assign rst_vip_m24_clk = cocotb_clock;

    // clk connect to RST-master[25] VIP
    assign rst_vip_m25_clk = cocotb_clock;

    // clk connect to RST-master[26] VIP
    assign rst_vip_m26_clk = cocotb_clock;

    // clk connect to RST-master[27] VIP
    assign rst_vip_m27_clk = cocotb_clock;

    // clk connect to RST-master[28] VIP
    assign rst_vip_m28_clk = cocotb_clock;

    // clk connect to RST-master[29] VIP
    assign rst_vip_m29_clk = cocotb_clock;

    // clk connect to RST-master[30] VIP
    assign rst_vip_m30_clk = cocotb_clock;

    // clk connect to RST-master[31] VIP
    assign rst_vip_m31_clk = cocotb_clock;

    // clk connect to RST-master[32] VIP
    assign rst_vip_m32_clk = cocotb_clock;

    // clk connect to RST-master[33] VIP
    assign rst_vip_m33_clk = cocotb_clock;

    // clk connect to RST-master[34] VIP
    assign rst_vip_m34_clk = cocotb_clock;

    // clk connect to RST-master[35] VIP
    assign rst_vip_m35_clk = cocotb_clock;

    // clk connect to RST-master[36] VIP
    assign rst_vip_m36_clk = cocotb_clock;

    // clk connect to RST-master[37] VIP
    assign rst_vip_m37_clk = cocotb_clock;

    // clk connect to RST-master[38] VIP
    assign rst_vip_m38_clk = cocotb_clock;

    // clk connect to RST-master[39] VIP
    assign rst_vip_m39_clk = cocotb_clock;

    // clk connect to RST-master[40] VIP
    assign rst_vip_m40_clk = cocotb_clock;

    // clk connect to RST-master[41] VIP
    assign rst_vip_m41_clk = cocotb_clock;

    // clk connect to RST-master[42] VIP
    assign rst_vip_m42_clk = cocotb_clock;

    // clk connect to RST-master[43] VIP
    assign rst_vip_m43_clk = cocotb_clock;

    // clk connect to RST-master[44] VIP
    assign rst_vip_m44_clk = cocotb_clock;

    // clk connect to RST-master[45] VIP
    assign rst_vip_m45_clk = cocotb_clock;

    // clk connect to RST-master[46] VIP
    assign rst_vip_m46_clk = cocotb_clock;

    // clk connect to RST-master[47] VIP
    assign rst_vip_m47_clk = cocotb_clock;

    // clk connect to RST-master[48] VIP
    assign rst_vip_m48_clk = cocotb_clock;

    // clk connect to RST-master[49] VIP
    assign rst_vip_m49_clk = cocotb_clock;

    // clk connect to RST-master[50] VIP
    assign rst_vip_m50_clk = cocotb_clock;

    // clk connect to RST-master[51] VIP
    assign rst_vip_m51_clk = cocotb_clock;

    // clk connect to RST-master[52] VIP
    assign rst_vip_m52_clk = cocotb_clock;

    // clk connect to RST-master[53] VIP
    assign rst_vip_m53_clk = cocotb_clock;

    // clk connect to RST-master[54] VIP
    assign rst_vip_m54_clk = cocotb_clock;

    // clk connect to RST-master[55] VIP
    assign rst_vip_m55_clk = cocotb_clock;

    // clk connect to RST-master[56] VIP
    assign rst_vip_m56_clk = cocotb_clock;

    // clk connect to RST-master[57] VIP
    assign rst_vip_m57_clk = cocotb_clock;

    // clk connect to RST-master[58] VIP
    assign rst_vip_m58_clk = cocotb_clock;

    // clk connect to RST-master[59] VIP
    assign rst_vip_m59_clk = cocotb_clock;

    // clk connect to RST-master[60] VIP
    assign rst_vip_m60_clk = cocotb_clock;

    // clk connect to RST-master[61] VIP
    assign rst_vip_m61_clk = cocotb_clock;

    // clk connect to RST-master[62] VIP
    assign rst_vip_m62_clk = cocotb_clock;

    // clk connect to RST-master[63] VIP
    assign rst_vip_m63_clk = cocotb_clock;

    // clk connect to RST-master[64] VIP
    assign rst_vip_m64_clk = cocotb_clock;

    // clk connect to RST-master[65] VIP
    assign rst_vip_m65_clk = cocotb_clock;

    // clk connect to RST-master[66] VIP
    assign rst_vip_m66_clk = cocotb_clock;

    // clk connect to RST-master[67] VIP
    assign rst_vip_m67_clk = cocotb_clock;

    // clk connect to RST-master[68] VIP
    assign rst_vip_m68_clk = cocotb_clock;

    // clk connect to RST-master[69] VIP
    assign rst_vip_m69_clk = cocotb_clock;

    // clk connect to RST-master[70] VIP
    assign rst_vip_m70_clk = cocotb_clock;

    // clk connect to RST-master[71] VIP
    assign rst_vip_m71_clk = cocotb_clock;

    // clk connect to RST-master[72] VIP
    assign rst_vip_m72_clk = cocotb_clock;

    // clk connect to RST-master[73] VIP
    assign rst_vip_m73_clk = cocotb_clock;

    // clk connect to RST-master[74] VIP
    assign rst_vip_m74_clk = cocotb_clock;

    // clk connect to RST-master[75] VIP
    assign rst_vip_m75_clk = cocotb_clock;

    // clk connect to RST-master[76] VIP
    assign rst_vip_m76_clk = cocotb_clock;

    // clk connect to RST-master[77] VIP
    assign rst_vip_m77_clk = cocotb_clock;

    // clk connect to RST-master[78] VIP
    assign rst_vip_m78_clk = cocotb_clock;

    // clk connect to RST-master[79] VIP
    assign rst_vip_m79_clk = cocotb_clock;

    // clk connect to RST-master[80] VIP
    assign rst_vip_m80_clk = cocotb_clock;

    // clk connect to RST-master[81] VIP
    assign rst_vip_m81_clk = cocotb_clock;

    // clk connect to RST-master[82] VIP
    assign rst_vip_m82_clk = cocotb_clock;

    // clk connect to RST-master[83] VIP
    assign rst_vip_m83_clk = cocotb_clock;

    // clk connect to RST-master[84] VIP
    assign rst_vip_m84_clk = cocotb_clock;

    // clk connect to RST-master[85] VIP
    assign rst_vip_m85_clk = cocotb_clock;

    // clk connect to RST-master[86] VIP
    assign rst_vip_m86_clk = cocotb_clock;

    // clk connect to RST-master[87] VIP
    assign rst_vip_m87_clk = cocotb_clock;

    // clk connect to RST-master[88] VIP
    assign rst_vip_m88_clk = cocotb_clock;

    // clk & rst connect to APB master
    assign apb_vip_m0_pclk = cocotb_pclock;
    assign apb_vip_m0_presetn = rst_vip_m7_reset;
    

    assign wdt_rst_n_layer[0] = rst_vip_m3_reset;
    assign wdt_rst_n_layer[1] = rst_vip_m4_reset;
    assign wdt_rst_n_layer[2] = rst_vip_m5_reset;
    assign wdt_rst_n_layer[3] = rst_vip_m6_reset;

    assign wdt_rst_n = wdt_rst_n_layer;

    assign rst_vip_m10_reset = rst_sb_i2c_n[0];
    assign rst_vip_m11_reset = rst_sb_i2c_n[1];

    assign rst_vip_m18_reset = rst_wdt_n[0];
    assign rst_vip_m19_reset = rst_wdt_n[1];
    assign rst_vip_m20_reset = rst_wdt_n[2];
    assign rst_vip_m21_reset = rst_wdt_n[3];

    assign rst_vip_m22_reset = rst_gpt_n[0];
    assign rst_vip_m23_reset = rst_gpt_n[1];
    assign rst_vip_m24_reset = rst_gpt_n[2];
    assign rst_vip_m25_reset = rst_gpt_n[3];
    assign rst_vip_m26_reset = rst_gpt_n[4];
    assign rst_vip_m27_reset = rst_gpt_n[5];
    assign rst_vip_m28_reset = rst_gpt_n[6];
    assign rst_vip_m29_reset = rst_gpt_n[7];

    assign rst_vip_m30_reset = rst_sram_n[0];

    assign rst_vip_m32_reset = rst_usb_n[0];
    assign rst_vip_m33_reset = rst_usb_n[1];
    assign rst_vip_m34_reset = rst_usb_n[2];
    assign rst_vip_m35_reset = rst_usb_n[3];

    assign rst_vip_m36_reset = rst_mmc_n[0];
    assign rst_vip_m37_reset = rst_mmc_n[1];
    assign rst_vip_m38_reset = rst_mmc_n[2];
    assign rst_vip_m39_reset = rst_mmc_n[3];

    assign rst_vip_m41_reset = rst_qspi_n[0];
    assign rst_vip_m42_reset = rst_qspi_n[1];

    assign rst_vip_m43_reset = rst_spi_n[0];
    assign rst_vip_m44_reset = rst_spi_n[1];
    assign rst_vip_m45_reset = rst_spi_n[2];
    assign rst_vip_m46_reset = rst_spi_n[3];
    assign rst_vip_m47_reset = rst_spi_n[4];
    assign rst_vip_m48_reset = rst_spi_n[5];

    assign rst_vip_m49_reset = rst_i2c_n[0];
    assign rst_vip_m50_reset = rst_i2c_n[1];
    assign rst_vip_m51_reset = rst_i2c_n[2];
    assign rst_vip_m52_reset = rst_i2c_n[3];
    assign rst_vip_m53_reset = rst_i2c_n[4];
    assign rst_vip_m54_reset = rst_i2c_n[5];
    assign rst_vip_m55_reset = rst_i2c_n[6];

    assign rst_vip_m56_reset = rst_uart_n[0];
    assign rst_vip_m57_reset = rst_uart_n[1];
    assign rst_vip_m58_reset = rst_uart_n[2];
    assign rst_vip_m59_reset = rst_uart_n[3];
    assign rst_vip_m60_reset = rst_uart_n[4];

    assign rst_vip_m61_reset = rst_gpio_n[0];
    assign rst_vip_m62_reset = rst_gpio_n[1];

    assign rst_vip_m63_reset = rst_pwm_n[0];
    assign rst_vip_m64_reset = rst_pwm_n[1];
    assign rst_vip_m65_reset = rst_pwm_n[2];

    assign rst_vip_m70_reset = rst_display_n[0];
    assign rst_vip_m71_reset = rst_display_n[1];

    assign rst_vip_m73_reset = rst_cpu_n[0];
    assign rst_vip_m74_reset = rst_cpu_n[1];
    assign rst_vip_m75_reset = rst_cpu_n[2];
    assign rst_vip_m76_reset = rst_cpu_n[3];
    assign rst_vip_m77_reset = rst_cpu_n[4];
    assign rst_vip_m78_reset = rst_cpu_n[5];
    assign rst_vip_m79_reset = rst_cpu_n[6];
    assign rst_vip_m80_reset = rst_cpu_n[7];

    assign rst_vip_m81_reset = rst_i2s_n[0];
    assign rst_vip_m82_reset = rst_i2s_n[1];
    assign rst_vip_m83_reset = rst_i2s_n[2];
    assign rst_vip_m84_reset = rst_i2s_n[3];
    assign rst_vip_m85_reset = rst_i2s_n[4];

`ifndef YMP_STUB

ymp_rgu_top 
#(
    .RGU_TIM0_DEF (TIM0),
    .RGU_TIM1_DEF (TIM1)
)
dut

(
    .clk      (cocotb_clock) , 
    .sys_pwrgd (rst_vip_m0_reset),
    .sys_reset_n (rst_vip_m1_reset),
    .sb_wdt_rst_n (rst_vip_m2_reset),
    .wdt_rst_n (wdt_rst_n), 
    .rst_sb_dmac_n (rst_vip_m8_reset),
    .rst_sb_qspi_n (rst_vip_m9_reset),
    .rst_sb_i2c_n (rst_sb_i2c_n), 
    .rst_sb_uart_n (rst_vip_m12_reset),
    .rst_sb_gpio_n (rst_vip_m13_reset),
    .rst_sb_sram_n (rst_vip_m14_reset),
    .rst_sb_wdt_n (rst_vip_m15_reset),
    .rst_sb_cpu_n (rst_vip_m16_reset),
    .rst_sys_n (rst_vip_m17_reset),
    .rst_wdt_n (rst_wdt_n), 
    .rst_gpt_n (rst_gpt_n),
    .rst_sram_n (rst_sram_n),
    .rst_ddr_n (rst_vip_m31_reset),
    .rst_usb_n (rst_usb_n), 
    .rst_mmc_n (rst_mmc_n), 
    .rst_dmac_n (rst_vip_m40_reset),
    .rst_qspi_n (rst_qspi_n), 
    .rst_spi_n (rst_spi_n), 
    .rst_i2c_n (rst_i2c_n), 
    .rst_uart_n (rst_uart_n), 
    .rst_gpio_n (rst_gpio_n), 
    .rst_pwm_n (rst_pwm_n), 
    .rst_gpu_n (rst_vip_m66_reset),
    .rst_videc_n (rst_vip_m67_reset),
    .rst_vicod_n (rst_vip_m68_reset),
    .rst_camera_n (rst_vip_m69_reset),
    .rst_display_n (rst_display_n),
    .rst_llc_n (rst_vip_m72_reset),
    .rst_cpu_n (rst_cpu_n),
    .rst_i2s_n (rst_i2s_n), 
    .rst_sb_sys_n (rst_vip_m86_reset),
    .rst_cpu_pwrup_n (rst_vip_m87_reset),
    .rst_cpu_pwrup_heavy_n (rst_vip_m88_reset),
    .i_test_mode (1'b0), 
    .i_dft_scan_mode (1'b0),
    .i_dft_test_rstn (1'b0),
    .PCLK (apb_vip_m0_pclk), 
    .PRESETn (apb_vip_m0_presetn),
    .PADDR (apb_vip_m0_paddr),
    .PWRITE (apb_vip_m0_pwrite),
    .PWDATA (apb_vip_m0_pwdata),
    .PSEL (apb_vip_m0_psel),
    .PENABLE (apb_vip_m0_penable),
    .PRDATA (apb_vip_m0_prdata),
    .PREADY (apb_vip_m0_pready),
    .PSLVERR (apb_vip_m0_pslverr)
);

`endif

endmodule
`endif
