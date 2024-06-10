import pandas as pd
import argparse

def readCSV(file):
    df = pd.read_csv(file)
    df.dropna(how="all").reset_index(drop=True)
    df.drop(['File_Index'], axis=1, inplace=True)
    return parseDatetime(df.copy())

def parseDatetime(df_dt):
    df_dt['Timestamp'] = df_dt['Timestamp'].str.split('.').str[0]
    print(df_dt['Timestamp'].head(20))
    return parseCodeFile(df_dt.copy())

def parseCodeFile(df_codefile):
    pass
    return parseFunction(df_codefile.copy())

def parseFunction(df_function):
    pass
    return writeCSV(df_function.copy())

def writeCSV(df):

    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='CSV file')
    args = parser.parse_args()
    readCSV(args.file)

if __name__ == '__main__':
    main()
