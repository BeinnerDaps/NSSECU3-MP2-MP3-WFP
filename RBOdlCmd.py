#!/usr/bin/env python3

import argparse
import subprocess
import os
import pandas as pd
import tempfile

def readCSV(file):
    df = pd.read_csv(file)
    df.dropna(how="all").reset_index(drop=True)
    df.drop(['File_Index'], axis=1, inplace=True)
    return parseDatetime(df.copy())

def parseDatetime(df_dt):
    df_dt['Timestamp'] = df_dt['Timestamp'].str.split('.').str[0]
    return parseFunction(df_dt.copy())

def parseFunction(df_func):
    df_func['Function'] = df_func['Function'].str.replace(r'(?<!^)(?=[A-Z])', ' ', regex=True).str.replace('::', ' -')
    return writeCSV(df_func.copy())

def writeCSV(df):
    with pd.ExcelWriter('output.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Parsed')
        workbook = writer.book
        worksheet = writer.sheets['Parsed']
        for col in df:
            colWidth = max(df[col].astype(str).map(len).max(), len(col))
            colWidth = 100 if colWidth > 100 else colWidth
            colIndex = df.columns.get_loc(col)
            worksheet.set_column(colIndex, colIndex, colWidth)
    print("DataFrame has been written to 'output.xlsx'")

def run_tool(tool, path, output_path, obfuscationstringmap_path, all_key_values, all_data):
    # Build the command based on the chosen tool
    if tool == 'odl':
        command = ['python', 'odl.py', path]
        if output_path:
            command.extend(['-o', output_path])
        if obfuscationstringmap_path:
            command.extend(['-s', obfuscationstringmap_path])
        if all_key_values:
            command.append('-k')
        if all_data:
            command.append('-d')
    elif tool == 'rb':
        command = ['RBCmd.exe', path]
        if output_path:
            command.extend(['-o', output_path])

    # Print the command for debugging
    print(f"Running command: {' '.join(command)}")

    # Execute the command
    try:
        result = subprocess.run(command, check=True)
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error running {tool}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Wrapper script to run odl.py or RBCmd.exe")
    parser.add_argument('tool', choices=['odl', 'rb'], help='Specify which tool to run: odl (odl.py) or rb (RBCmd.exe)')
    parser.add_argument('path', help='Path to folder with .odl files for odl.py or to file to process with RBCmd.exe')
    parser.add_argument('-s', '--obfuscationstringmap_path', help='Path to ObfuscationStringMap.txt (if not in odl_folder)', default='')
    parser.add_argument('-k', '--all_key_values', action='store_true', help='For repeated keys in ObfuscationMap, get all values | delimited (off by default)')
    parser.add_argument('-d', '--all_data', action='store_true', help='Show all data (off by default)')
    
    args = parser.parse_args()

    # Create a temporary file for the CSV output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_csv:
        output_path = temp_csv.name

    # Run the tool and generate the CSV
    run_tool(args.tool, args.path, output_path, args.obfuscationstringmap_path, args.all_key_values, args.all_data)

    # Process the generated CSV
    readCSV(output_path)

if __name__ == "__main__":
    main()
