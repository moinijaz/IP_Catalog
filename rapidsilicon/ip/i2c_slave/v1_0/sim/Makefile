# This file is Copyright (c) 2022 RapidSilicon.
#
# SPDX-License-Identifier: MIT
MODULE_NAME ?= i2c_slave

OUT_DIR ?= $(PWD)

all:
	@sed -i "s|test_i2c_slave_axil_master.lxt|$(OUT_DIR)/test_i2c_slave_axil_master.lxt|g" ./test_i2c_slave_axil_master.v
	@python3 test_i2c.py && echo "TEST 1 PASSED" || echo "TEST 1 FAILED"
	-@python3 test_i2c_slave_axil_master.py && echo "TEST 2 PASSED" || echo "TEST 2 FAILED"
	-@mv test_i2c_slave_axil_master.vvp $(OUT_DIR)
	-@mv test_i2c.vcd $(OUT_DIR)
	@sed -i "s|$(OUT_DIR)/test_i2c_slave_axil_master.lxt|test_i2c_slave_axil_master.lxt|g" ./test_i2c_slave_axil_master.v
clear:
	@rm -rf __pycache__ *.lxt *.vvp *.vcd rapidsilicon ../litex_wrapper/__pycache__