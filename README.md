# pyHYControl
Python3 module to interact with Huanyang VFD controllers over RS485.

This module can talk the "chinese pseudo-modbus" protocol that Huanyang
tries to sell you as Modbus-compatible.

The goal is to make configuring the VFD easier than punching in all register
values through the control panel.

I recommend that you set the following parameters by hand before attempting to communicate
(thanks [Bouni](https://gist.github.com/Bouni/803492ed0aab3f944066#file-hunayang-rs485-commands-md) and the guys at [LinuxCNC](https://github.com/LinuxCNC/linuxcnc)):

 - PD163: 1 (Communication address: 1)
 - PD164: 1 (Communication Baud Rate: 9600)
 - PD165: 3 (Communication Data Method: 8N1 RTU)

Afterwards, communicating with the VFD controller through an RS232 to RS485 converter is straightforward.

# hycontrol command
The command line utility in this module can be used with `python3 -m hycontrol [options] subcommand <command parameters>`.
Use the `-h` option or no option and subcommand to display the command help.

# classes
You can also use the classes directly, see `hycontrol.config` for configuration related classes like device parameters and the register map and `hycontrol.device` for the `VFDDevice` class that handles communication with the VFD.
