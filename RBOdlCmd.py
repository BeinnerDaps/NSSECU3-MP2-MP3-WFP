#!/usr/bin/env python3
import os
import subprocess



# Run odl.py with command line arguments
odl_args = ["python", "/path/to/odl.py", "arg1", "arg2"]
subprocess.run(odl_args)

# Run rbcmd.exe with command line arguments
rbcmd_args = ["/path/to/rbcmd.exe", "arg1", "arg2"]
subprocess.run(rbcmd_args)