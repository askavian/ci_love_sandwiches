# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread # imports entire google spreadsheet
from google.oauth2.service_account import Credentials # imports only credentials functions 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ci_love_sandwiches')

#sales = SHEET.worksheet('sales')                               #  test if API is working
#data = sales.get_all_values()                                  #  test if API is working
#print(data)                                                    #  test if API is working

def get_sales_data():
    """
    Get sales figures input from the user
    """
    print("Please enter the sales data from the last market.")
    print("Data should be six numbers, seperated by commas.")
    print("Example: 10,20,30,40,50,60\n")                       #  \n = New Line Character

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")                   #  f string for interpolation of values 

get_sales_data()