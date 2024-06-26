/*

Copyright (c) 2016-2018 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

*/

// Language: Verilog 2001

`resetall
`timescale 1ns / 1ps
`default_nettype none

/*
 * Generic source synchronous SDR input
 */
module ssio_sdr_in #
(
    // Width of register in bits
    parameter WIDTH = 1
)
(
    input  wire             input_clk,

    input  wire [WIDTH-1:0] input_d,

    output wire             output_clk,

    output wire [WIDTH-1:0] output_q
);

wire clk_int;
wire clk_io;

CLK_BUF 
CLK_BUF_inst(
    .I(input_clk),
    .O(output_clk)
);

CLK_BUF 
CLK_BUF_inst_1(
    .I(input_clk),
    .O(clk_io)
);

reg [WIDTH-1:0] output_q_reg = {WIDTH{1'b0}};

assign output_q = output_q_reg;

always @(posedge clk_io) begin
    output_q_reg <= input_d;
end

endmodule

`resetall
