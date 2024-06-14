#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys
import pandas as pd
import tempfile

def readCSV(file, output_path):
    try:
        df = pd.read_csv(file)
        df.dropna(how="all", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop(['File_Index'], axis=1, inplace=True)
        return parseDatetime(df.copy(), output_path)
    except PermissionError as e:
        print(f"Permission Denied: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def parseDatetime(df_dt, output_path):
    df_dt['Timestamp'] = df_dt['Timestamp'].str.split('.').str[0]
    return parseFunction(df_dt.copy(), output_path)

def parseFunction(df_func, output_path):
    df_func['Function'] = df_func['Function'].str.replace(r'(?<!^)(?=[A-Z])', ' ', regex=True).str.replace('::', ' -')
    return writeCSV(df_func.copy(), output_path)

def writeCSV(df, output_path):
    output = os.path.join(output_path, 'output.xlsx')
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Parsed')
        worksheet = writer.sheets['Parsed']
        for col in df:
            colWidth = max(df[col].astype(str).map(len).max(), len(col))
            colWidth = 100 if colWidth > 100 else colWidth
            colIndex = df.columns.get_loc(col)
            worksheet.set_column(colIndex, colIndex, colWidth)
    print(f"DataFrame has been written to {output}")

def run_tool(tool, path, output_path, obfuscationstringmap_path, all_key_values, all_data):
    if tool == 'odl':
        with tempfile.NamedTemporaryFile(delete=True, suffix=".csv") as temp_csv:
            output_file = temp_csv.name
        commands = [['python', 'odl.py', path, '-o', output_file]]
        if obfuscationstringmap_path:
            commands[0].extend(['-s', obfuscationstringmap_path])
        if all_key_values:
            commands[0].append('-k')
        if all_data:
            commands[0].append('-d')
    elif tool == 'rb':
        new_path = os.path.join(r"C:\$Recycle.Bin", path)
        new_folder = os.path.join(output_path, 'RBCMetaData')
        try:
            os.makedirs(new_folder)
            print(f"Directory {new_folder} created successfully.")
        except OSError as error:
            print(error)

        commands = [
            ['cd', new_path],
            ['copy', "$I*", new_folder],
            ['cd', output_path],
            ['RBCmd.exe', '-d', new_folder, '--csv', output_path]
        ]

    runParsers(commands)
    if tool == 'odl':
        readCSV(output_file, output_path)

def runParsers(commands):
    try:
        for command in commands:
            print('Running command: {' '.join(command)}')
            if command[0] == 'cd':
                os.chdir(command[1])
            else:
                subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Wrapper script to run odl.py or RBCmd.exe")
    parser.add_argument('tool', choices=['odl', 'rb'], help='Specify which tool to run: odl (odl.py) or rb (RBCmd.exe)')
    parser.add_argument('path', help='Path to folder with .odl logs for odl or Path to recycle bin with $I files for rb')
    parser.add_argument('-o', '--output_path', help='Path to output', default=None)
    parser.add_argument('-s', '--obfuscationstringmap_path', help='Path to ObfuscationStringMap.txt (if not in odl_folder)', default=None)
    parser.add_argument('-k', '--all_key_values', action='store_true', help='For repeated keys in ObfuscationMap, get all values | delimited (off by default)')
    parser.add_argument('-d', '--all_data', action='store_true', help='Show all data (off by default)')
    args = parser.parse_args()

    if args.output_path is None:
        output_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    run_tool(args.tool, args.path, output_path, args.obfuscationstringmap_path, args.all_key_values, args.all_data)

if __name__ == "__main__":
    main()
