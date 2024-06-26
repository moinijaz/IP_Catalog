# Copyright (c) 2020 Alex Forencich
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

TOPLEVEL_LANG = verilog

SIM ?= icarus
WAVES ?= 1

COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

DUT      = top
TOPLEVEL = $(DUT)
MODULE   = test_$(DUT)
VERILOG_SOURCES += $(DUT).v
VERILOG_SOURCES += ../src/eth_mac_1g_gmii.v
VERILOG_SOURCES += ../src/gmii_phy_if.v
VERILOG_SOURCES += ../src/ssio_sdr_in.v
VERILOG_SOURCES += ../src/ssio_sdr_out.v
VERILOG_SOURCES += ../src/oddr.v
VERILOG_SOURCES += ../src/eth_mac_1g.v
VERILOG_SOURCES += ../src/axis_gmii_rx.v
VERILOG_SOURCES += ../src/axis_gmii_tx.v
VERILOG_SOURCES += ../src/lfsr.v
VERILOG_SOURCES += ../src/mac_ctrl_rx.v
VERILOG_SOURCES += ../src/mac_ctrl_tx.v
VERILOG_SOURCES += ../src/mac_pause_ctrl_rx.v
VERILOG_SOURCES += ../src/mac_pause_ctrl_tx.v
VERILOG_SOURCES += CLK_BUF.v
VERILOG_SOURCES += O_DDR.v

ifeq ($(SIM), icarus)
	PLUSARGS += -fst

	COMPILE_ARGS += $(-P $(TOPLEVEL).$(subst PARAM_,,$(v))=$($(v)))

	ifeq ($(WAVES), 1)
		VERILOG_SOURCES += iverilog_dump.v
		COMPILE_ARGS += -s iverilog_dump
	endif
else ifeq ($(SIM), verilator)
	COMPILE_ARGS += -Wno-SELRANGE -Wno-WIDTH --timing -Wno-fatal

	COMPILE_ARGS += $(foreach v,$(filter PARAM_%,$(.VARIABLES)),-G$(subst PARAM_,,$(v))=$($(v)))

	ifeq ($(WAVES), 1)
		COMPILE_ARGS += --trace-fst
	endif
endif

include $(shell cocotb-config --makefiles)/Makefile.sim

iverilog_dump.v:
	echo 'module iverilog_dump();' > $@
	echo 'initial begin' >> $@
	echo '    $$dumpfile("$(SIM_BUILD)/$(TOPLEVEL).fst");' >> $@
	echo '    $$dumpvars(0, $(TOPLEVEL));' >> $@
	echo 'end' >> $@
	echo 'endmodule' >> $@

clean::
	@rm -rf iverilog_dump.v
	@rm -rf dump.fst $(TOPLEVEL).fst
	@rm -rf *_wrap_*.v
	@rm -rf rapidsilicon/
	@rm -rf __pycache__
	@rm -rf results.xml
	@rm -rf ../litex_wrapper/__pycache__ 
