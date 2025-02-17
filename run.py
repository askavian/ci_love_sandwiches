# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread                                                  #  imports entire google spreadsheet
from google.oauth2.service_account import Credentials           #  imports only credentials functions 

SCOPE = [                                                       #  is selected in the API Library on Google API & Services page
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')     #  links to .json file where API Acces credentials is stored
SCOPED_CREDS = CREDS.with_scopes(SCOPE)                         #  calls the defined scope -> see above
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)                #  checks the credentials against Google API AIM Service
SHEET = GSPREAD_CLIENT.open('ci_love_sandwiches')               #  loads the spreadsheet if API AIM validation is successfull

#sales = SHEET.worksheet('sales')                               #  TEST: if API is working
#data = sales.get_all_values()                                  #  TEST: if API is working
#print(data)                                                    #  TEST: if API is working

def get_sales_data():
    """
    Get sales figures input from the user
    """
    print("Please enter the sales data from the last market.")
    print("Data should be six numbers, seperated by commas.")
    print("Example: 10,20,30,40,50,60\n")                       #  "\n" = New Line Character

    data_str = input("Enter your data here: ")                  #  input MUST BE exactly 6 Int
    #print(f"The data provided is {data_str}")                  #  TEST: "f" string for interpolation of values 

    sales_data = data_str.split(",")                            #  REMOVES string-"," and ADDS list-"," creates "data_str" list
    validate_data(sales_data)                                   #  calls "validate_data" function from inside "get_sales_data" function


def validate_data(values):                                      #  validates data function ("values" is relative to where function is called from)
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
#    print(values)                                              # TEST: for raw values input
    try:
        [int(value) for value in values]                        #  converts all values in list to integer 
        if len(values) != 6:                                    #  if the values (list) IS NOT exactly 6 numbers     
            raise ValueError(                                   #  raises ValueError and shows lenght given            
                f"Exactly 6 values required, you provided {len(values)}"
            ) 
    except ValueError as e:                                     #  "e" is Python shorthand for ERROR    
        print(f"Invalid data: {e}, please try again.\n")        #  combines "raise ValueError" into statement wie "e" keyword                 

get_sales_data()