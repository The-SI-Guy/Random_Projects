# AudioBeamforming

## scripts descriptions

A few scripts going towards beamforming an Audio Array whether that ends up being microphones or speakers

- Python code can be seen in the python folder
- Verilog code is in the verilog folder

## Future plans

- Decide on an FPGA to get perhaps Pynq Z2, and possibly one of the PMOD microphones Digilent sells for testing FIR Filters before implementing a custom additional oard
- Create verilog code for the FIR filters to go into an FPGA 
- Create verilog code for talking to a future PCB with microphones/ADC's or speakers/DAC's
- Learn how to pipe the data out of the FPGA SoC straight off the board or through the linux subsystem
- Create a PCB with some MEMS Isotropic microphones/ADC's or speakers/DAC's to hook up to the FPGA


