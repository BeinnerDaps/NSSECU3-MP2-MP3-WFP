#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys
import tempfile
import ctypes
import shutil
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch the script with administrative privileges."""
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
    try:
        subprocess.run(["runas", "/user:Administrator", f'python {script} {params}'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to elevate to admin: {e}")
        sys.exit(1)

def readCSV(file, output_path, path, tool):
    """reading CSV file for Parsing"""
    try:
        df = pd.read_csv(file)
        df.dropna(how="all", inplace=True)
        df.reset_index(drop=True, inplace=True)
        if tool == 'odl':
            return parseOdl(df.copy(), output_path, path)
        elif tool == 'rb':
            return parseRb(df.copy(), output_path, path)
    except PermissionError as e:
        print(f"Permission Denied: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def parseOdl(df_odl, output_path, path):
    """Parsing ODL file"""
    try:
        df_odl.drop(['File_Index'], axis=1, inplace=True)
        df_odl['Filename'] = df_odl['Filename'].apply(lambda x: os.path.join(path, x))
        df_odl['Timestamp'] = df_odl['Timestamp'].str.split('.').str[0]
        df_odl['Function'] = df_odl['Function'].str.replace(r'(?<!^)(?=[A-Z])', ' ', regex=True).str.replace('::', ' -')
        df_odl = move_column_to_first(df_odl, 'Timestamp')
        df_odl = df_odl.sort_values(by='Timestamp', ascending=False)
        return writeCSV(df_odl.copy(), output_path, 'Parsed_odl.xlsx')
    except Exception as e:
        print(f"An error occurred: {e}")

def parseRb(df_rb, output_path, path):
    """Parsing RBCmd file"""
    try:
        df_rb['UserSID'] = f'{path}'
        df_rb = move_column_to_first(df_rb, 'UserSID')
        df_rb = move_column_to_first(df_rb, 'DeletedOn')
        df_rb = df_rb.sort_values(by='DeletedOn', ascending=False)
        return writeCSV(df_rb.copy(), output_path, 'Parsed_rb.xlsx')
    except Exception as e:
        print(f"An error occurred: {e}")

def writeCSV(df, output_path, filename):
    """Writing RBCmd or Odl file"""
    try:
        output = os.path.join(output_path, filename)
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Parsed')
            worksheet = writer.sheets['Parsed']
            for col in df:
                colWidth = max(df[col].astype(str).map(len).max(), len(col))
                colWidth = 100 if colWidth > 100 else colWidth
                colIndex = df.columns.get_loc(col)
                worksheet.set_column(colIndex, colIndex, colWidth)
        print(f"DataFrame has been written to {output}")
    except Exception as e:
        print(f"An error occurred: {e}")

def move_column_to_first(df, column_name):
    if column_name in df.columns:
        columns = [column_name] + [col for col in df.columns if col != column_name]
        df = df[columns]
    return df

def run_tool(args):
    tool, path, output_path, obf, all_kval, all_data = args
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_csv:
        output_file = temp_csv.name
        temp_directory = os.path.dirname(output_file)

    if 'odl' == tool:
        odl = ['python', 'odl.py', path, '-o', output_file]
        if obf: odl.extend(['-s', obf])
        if all_kval: odl.append('-k')
        if all_data: odl.append('-d')
        commands = [odl]

    if 'rb' == tool:
        path = os.path.join(r"C:\$Recycle.Bin", path)
        new_folder = os.path.join(output_path, 'RBCMetaData')
        temp_directory = output_path
        try:
            os.makedirs(new_folder)
            print(f"Directory {new_folder} created successfully.")
        except OSError as error:
            print(error)

        commands = [
            ['cd', path],
            ['copy', "$I*", new_folder],
            ['cd', defaultpath()],
            [r'.\RBCmd.exe', '-d', new_folder, '--csv', temp_directory]
        ]

    runParsers(commands, temp_directory, output_path, path, tool)
    if tool == 'rb': shutil.rmtree('RBCMetaData')

def runParsers(commands, directory, output_path, path, tool):
    try:
        for command in commands:
            print(f'Running command: {" ".join(command)}')
            if command[0] == 'cd':
                os.chdir(command[1])
            else:
                result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)

        if result.returncode != 0:
            print(f"Command failed with return code {result.returncode}")
            print(f"Error output: {result.stderr}")
            return None

        output = result.stdout.strip()
        filename = os.path.basename(output)
        output_file = os.path.join(directory, filename)
        print(f'Filename: {filename}')
        print(f'directory: {output_file}')
        readCSV(output_file, output_path, path, tool)
        os.remove(output_file)

    except subprocess.CalledProcessError as e:
        print(e)

def defaultpath():
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def main():
    if not is_admin():
        print("Not running as admin, attempting to relaunch with admin privileges...")
        run_as_admin()
        return

    parser = argparse.ArgumentParser(description="Wrapper script to run odl.py or RBCmd.exe")
    parser.add_argument('-t', '--tool', metavar=('tool1', 'tool2'), nargs='*', help='Specify which tool to run: odl (odl.py), rb (RBCmd.exe)', choices=['odl','rb'], default=None)
    parser.add_argument('-p', '--path', metavar=('path1', 'path2'), nargs='*', help='Path to .odl logs folder for odl or user SID for rb', default=None)
    parser.add_argument('-o', '--output_path', help='Path to output', default=None)
    parser.add_argument('-s', '--obfstrmap', help='Path to ObfuscationStringMap.txt (if not in odl_folder)', default=None)
    parser.add_argument('-k', '--all_key_values', action='store_true', help='For repeated keys in ObfuscationMap, get all values | delimited (off by default)', default=False)
    parser.add_argument('-d', '--all_data', action='store_true', help='Show all data (off by default)', default=False)
    args = parser.parse_args()

    tools = args.tool
    paths = args.path
    output_path = args.output_path or defaultpath()
    if not len(tools) == len(paths):
        parser.error('Both --tools and --paths must be provided with the same number of values.')

    arguments = []
    for tool, path in zip(tools, paths):
        arguments.append([tool, path, output_path, args.obfstrmap, args.all_key_values, args.all_data])

    with ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(run_tool, arguments), total=len(arguments), desc="Processing files"))

if __name__ == "__main__":
    main()
