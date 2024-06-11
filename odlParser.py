import pandas as pd
import argparse

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
            colWidth = max(df[col].astype(str).map(len).max(),len(col))
            colWidth = 100 if colWidth > 100 else colWidth
            colIndex = df.columns.get_loc(col)
            worksheet.set_column(colIndex, colIndex, colWidth)
    print("DataFrame has been written to 'output.xlsx'")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='CSV file')
    args = parser.parse_args()
    readCSV(args.file)

if __name__ == '__main__':
    main()
