# because I am lazy to convert csv to excel
# real reason is that I want to use the excel file to do some data analysis
import pandas as pd
import os
import sys

# # Defile the path of the csv file
# CSV = 'endpoint_api.csv'
# EXCEL = 'endpoint_api.xlsx'


# Check if any argument is passed
if len(sys.argv) == 1:
    print('No argument passed')
    # print the usage
    print('Usage: python csv-to-excel.py <csv file>')
    sys.exit()

# pass the csv file as an argument
CSV = sys.argv[1]
# Check if the csv file passed as an argument
if not os.path.exists(CSV):
    print('CSV file does not exist')
    # print the usage
    print('Usage: python csv-to-excel.py <csv file>')
    print('If file contains spaces use double quotes')
    sys.exit()


# excel file name will be same as csv file name
EXCEL = CSV.split('.')[0] + '.xlsx'
# if excel file already exists then rename it
if os.path.exists(EXCEL):
    EXCEL = EXCEL.split('.')[0] + '_1.xlsx'

# Read the csv file
read_file = pd.read_csv(CSV)


# Convert the csv file to excel
read_file.to_excel(EXCEL, index=None, header=True)
