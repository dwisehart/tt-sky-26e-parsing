# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Exercise the placeholder at the project's 25 MHz clock target.
    clock = Clock(dut.clk, 40, unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test development placeholder: 8-bit combinational adder")
    # Carry propagation, wraparound, and all operand bits, with settling
    # time for both RTL and the gate-level netlist.
    values = [0, 1, 2, 7, 15, 31, 63, 127, 128, 129, 254, 255]
    for ena, rst_n in [(1, 1), (0, 1), (1, 0), (0, 0)]:
        dut.ena.value = ena
        dut.rst_n.value = rst_n
        for a in values:
            for b in values:
                dut.ui_in.value = a
                dut.uio_in.value = b
                await Timer(200, unit="ns")
                assert int(dut.uo_out.value) == (a + b) & 0xFF
                assert int(dut.uio_out.value) == 0
                assert int(dut.uio_oe.value) == 0
