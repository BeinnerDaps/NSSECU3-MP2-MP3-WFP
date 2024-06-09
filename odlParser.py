import csv
import pandas as pd
import argparse

def getColumns(file):
    df = pd.read_csv(file)
    fileName = df['Filename'].tolist()
    fileIndex = df['File_Index'].tolist()
    timeStamp = df['Timestamp'].tolist()
    codeFile = df['Code_File'].tolist()
    function = df['Function'].tolist()

    pfileName = parseFile(fileName)
    ptimeStamp = parseTimeStamp(timeStamp)
    pcodeFile = parseCodeFile(codeFile)
    pfunction = parseFunction(function)

    writeCSV(pfileName, fileIndex, ptimeStamp, pcodeFile, pfunction)

def parseFile(fileName):
    pass

def parseTimeStamp(timeStamp):
    pass

def parseCodeFile(codeFile):
    pass

def parseFunction(function):
    pass

def writeCSV(pfileName, pfileIndex, ptimeStamp, pcodeFile, pfunction):
    if len(pfileName) == len(pfileIndex) == len(ptimeStamp) == len(pcodeFile) == len(pfunction):
        rows = zip(pfileName, pfileIndex, ptimeStamp, pcodeFile, pfunction)
        header = ["Filename", "File_Index", "Timestamp", "Code_File", "Function"]

        with open('Parsed_ODL_Report.csv', mode='w', newline='') as newFile:
            writer = csv.writer(newFile)
            writer.writerow(header)
            writer.writerows(rows)

        print("CSV file created successfully.")
    else:
        print("Error: All lists must be of the same length.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=float, help='The first argument.')
    args = parser.parse_args()
    getColumns(args.file)

if __name__ == '__main__':
    main()
