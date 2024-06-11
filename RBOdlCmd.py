#!/usr/bin/env python3

import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Wrapper script to run odl.py or RBCmd.exe")
    parser.add_argument('tool', choices=['odl', 'rb'], help='Specify which tool to run: odl (odl.py) or rb (RBCmd.exe)')
    parser.add_argument('path', help='Path to folder with .odl files or to file to process with RBCmd.exe')
    parser.add_argument('-o', '--output_path', help='Output file name and path', default='')
    parser.add_argument('-s', '--obfuscationstringmap_path', help='Path to ObfuscationStringMap.txt (if not in odl_folder)', default='')
    parser.add_argument('-k', '--all_key_values', action='store_true', help='For repeated keys in ObfuscationMap, get all values | delimited (off by default)')
    parser.add_argument('-d', '--all_data', action='store_true', help='Show all data (off by default)')
    
    args = parser.parse_args()

    if args.tool == 'odl':
        command = ['python', 'odl.py', args.path]
        if args.output_path:
            command.extend(['-o', args.output_path])
        if args.obfuscationstringmap_path:
            command.extend(['-s', args.obfuscationstringmap_path])
        if args.all_key_values:
            command.append('-k')
        if args.all_data:
            command.append('-d')
    elif args.tool == 'rb':
        command = ['RBCmd.exe', args.path]
        if args.output_path:
            command.extend(['-o', args.output_path])

    print(f"Running command: {' '.join(command)}")

    try:
        result = subprocess.run(command, check=True)
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error running {args.tool}: {e}")

if __name__ == "__main__":
    main()
