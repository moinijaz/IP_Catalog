#!/usr/bin/env python3
#
# This file is Copyright (c) 2022 RapidSilicon.
#
# SPDX-License-Identifier: MIT

import os
import sys
import json
import argparse

from litex_wrapper.axis_pipeline_register_litex_wrapper import AXISPIPELINEREGISTER

from migen import *

from litex.build.generic_platform import *

from litex.build.osfpga import OSFPGAPlatform

from litex.soc.interconnect.axi import AXIStreamInterface

# IOs/Interfaces -----------------------------------------------------------------------------------

def get_clkin_ios():
    return [
        ("clk",  0, Pins(1)),
        ("rst",  0, Pins(1)),
    ]

# AXIS_PIPELINE_REGISTER Wrapper ----------------------------------------------------------------------------------
class AXISPIPELINEREGISTERWrapper(Module):
    def __init__(self, platform, data_width, last_en, id_en, id_width, 
                dest_en, dest_width, user_en, user_width, reg_type, length
                ):
        # Clocking ---------------------------------------------------------------------------------
        platform.add_extension(get_clkin_ios())
        self.clock_domains.cd_sys  = ClockDomain()
        self.comb += self.cd_sys.clk.eq(platform.request("clk"))
        self.comb += self.cd_sys.rst.eq(platform.request("rst"))
        
        # AXI STREAM -------------------------------------------------------------------------------
        s_axis = AXIStreamInterface(
            data_width = data_width,
            user_width = user_width,
            dest_width = dest_width,
            id_width   = id_width
        )
        
        m_axis = AXIStreamInterface(
            data_width = data_width,
            user_width = user_width,
            dest_width = dest_width,
            id_width   = id_width
        )
        
        # Input AXI
        platform.add_extension(s_axis.get_ios("s_axis"))
        self.comb += s_axis.connect_to_pads(platform.request("s_axis"), mode="slave")
        
        # Output AXI
        platform.add_extension(m_axis.get_ios("m_axis"))
        self.comb += m_axis.connect_to_pads(platform.request("m_axis"), mode="master")
        
        # AXIS-PIPELINE-REGISTER ----------------------------------------------------------------------------------
        self.submodules += AXISPIPELINEREGISTER(platform,
            m_axis          = m_axis,
            s_axis          = s_axis,
            last_en         = last_en,
            id_en           = id_en,
            dest_en         = dest_en,
            user_en         = user_en,
            reg_type        = reg_type,
            length          = length
            )
        

# Build --------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="AXIS PIPELINE REGISTER CORE")

    # Import Common Modules.
    common_path = os.path.join(os.path.dirname(__file__), "..", "..")
    sys.path.append(common_path)

    from rapidsilicon.lib.common import IP_Builder

    # Core Parameters.
    core_group = parser.add_argument_group(title="Core parameters")
    core_group.add_argument("--data_width", type=int, default=8, choices=range(1,4097),  help="Data Width.")
    core_group.add_argument("--last_en",    type=int, default=1, choices=range(2),       help="Last Enable.")
    core_group.add_argument("--id_en",      type=int, default=0, choices=range(2),       help="ID Enable.")
    core_group.add_argument("--id_width",   type=int, default=8, choices=range(1, 33),   help="ID Width.")
    core_group.add_argument("--dest_en",    type=int, default=0, choices=range(2),       help="Destination Enable.")
    core_group.add_argument("--dest_width", type=int, default=8, choices=range(1, 33),   help="Destination Width.")
    core_group.add_argument("--user_en",    type=int, default=1, choices=range(2),       help="User Enable.")
    core_group.add_argument("--user_width", type=int, default=1, choices=range(1, 4097), help="User Width.")
    core_group.add_argument("--reg_type",   type=int, default=2, choices=range(3),       help="Register Type; 0 to bypass, 1 for simple buffer, 2 for skid buffer")
    core_group.add_argument("--length",     type=int, default=2, choices=range(6),       help="Number of registers in pipeline.")

    # Build Parameters.
    build_group = parser.add_argument_group(title="Build parameters")
    build_group.add_argument("--build",         action="store_true",                        help="Build Core")
    build_group.add_argument("--build-dir",     default="./",                               help="Build Directory")
    build_group.add_argument("--build-name",    default="axis_pipeline_register_wrapper",   help="Build Folder Name, Build RTL File Name and Module Name")

    # JSON Import/Template
    json_group = parser.add_argument_group(title="JSON Parameters")
    json_group.add_argument("--json",                                           help="Generate Core from JSON File")
    json_group.add_argument("--json-template",  action="store_true",            help="Generate JSON Template")

    args = parser.parse_args()

    # Import JSON (Optional) -----------------------------------------------------------------------
    if args.json:
        with open(args.json, 'rt') as f:
            t_args = argparse.Namespace()
            t_args.__dict__.update(json.load(f))
            args = parser.parse_args(namespace=t_args)

    # Export JSON Template (Optional) --------------------------------------------------------------
    if args.json_template:
        print(json.dumps(vars(args), indent=4))

    # Create Wrapper -------------------------------------------------------------------------------
    platform = OSFPGAPlatform(io=[], toolchain="raptor", device="gemini")
    module   = AXISPIPELINEREGISTERWrapper(platform,
        data_width = args.data_width,
        last_en    = args.last_en,
        id_en      = args.id_en,
        id_width   = args.id_width,
        dest_en    = args.dest_en,
        dest_width = args.dest_width,
        user_en    = args.user_en,
        user_width = args.user_width,
        reg_type   = args.reg_type,
        length     = args.length,
    )

    # Build Project --------------------------------------------------------------------------------
    if args.build:
        rs_builder = IP_Builder(device="gemini", ip_name="axis_pipeline_register", language="verilog")
        rs_builder.prepare(
            build_dir  = args.build_dir,
            build_name = args.build_name,
        )
        rs_builder.copy_files(gen_path=os.path.dirname(__file__))
        rs_builder.generate_tcl()
        rs_builder.generate_wrapper(
            platform   = platform,
            module     = module,
        )

if __name__ == "__main__":
    main()
