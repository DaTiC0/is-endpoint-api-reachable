# because I am lazy to convert csv to excel
# real reason is that I want to use the excel file to do some data analysis
import pandas as pd

# Defile the path of the csv file
CSV = 'merchant_api.csv'
EXCEL = 'merchant_api.xlsx'

# Read the csv file
read_file = pd.read_csv(CSV)

# Convert the csv file to excel
read_file.to_excel(EXCEL, index = None, header=True)