import pandas as pd
import argparse

def getColumns(file):
    df = pd.read_csv(file)
    fileName = df['Filename'].tolist()
    fileIndex = df['File_Index'].tolist()
    timeStamp = df['Timestamp'].tolist()
    codeFile = df['Code_File'].tolist()
    _function = df['Function'].tolist()

    return [fileName, fileIndex, codeFile, timeStamp, _function]

def parseFile(fileName):
    pass

def parseTimeStamp(timeStamp):
    pass

def parseCodeFile(codeFile):
    pass

def parseFunction(_function):
    pass

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=float, help='The first argument.')
    getColumns()

if __name__ == '__main__':
    main()
