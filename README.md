# NSSECU3_Git
NSSECU3 group 12 project folder

python 3.7+

pip install libraries
- construct
- pycryptodome
- argparse
- subprocess
- os
- sys
- tempfile
- ctypes
- shutil
- pandas
- tqdm
- concurrent

arguments
'-t'<tool>, 	'--tool' 		    - Specify which tool, choices: odl (odl.py) and/or rbc (RBCmd.exe)
'-p <path>',	'--path' 		    - Path to ODL logs or Recycle Bin UserSID
'-o <path>', 	'--output_path' 	- Path to output directory
'-s <hive>', 	'--obfstrmap' 	    - (ODL only) Path to ObfuscationStringMap.txt or general.keynote if not in odl_folder (off by default)
'-k <hive>', 	'--all_key_values' 	- (ODL only) For repeated keys in ObfuscationMap, get all values | delimited (off by default)
'-d <hive>', 	'--all_data' 	    - (ODL only) Show all data (off by default)

(NOTE: If '--output_path' is not given, default directory will be exe directory)
(NOTE: To get UserSID, refer to https://www.precysec.com/post/how-to-recover-deleted-files-windows-recycle-bin-forensics)

examples:
.\RBCmdOdlParser.exe -t odl -p "C:\Users\student\AppData\Local\Microsoft\OneDrive\logs\Business1" -d
- Parses all ODL logs to the default directory

.\RBCmdOdlParser.exe -t rbc -p "S-1-5-21-24768837-1461444044-554365501-1001" -o "path\to\output_folder"
- Parses Recycle Bin files to the output_folder

.\RBCmdOdlParser.exe -t odl -p "C:\Users\student\AppData\Local\Microsoft\OneDrive\logs\Business1" -s "path\to\directory\general.keynote" -d -k
- Parses all ODL logs with repeated keys using general.keynote

.\RBCmdOdlParser.exe -t odl rbc -p "C:\Users\student\AppData\Local\Microsoft\OneDrive\logs\Business1" "S-1-5-21-24768837-1461444044-554365501-1001" -o "path\to\output_folder" -d
- Parses all ODL logs and Recycle Bin files into a single output_folder
