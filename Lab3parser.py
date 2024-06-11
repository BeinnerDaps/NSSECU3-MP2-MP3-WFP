import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='CSV file')
    args = parser.parse_args()

if __name__ == '__main__':
    main()
