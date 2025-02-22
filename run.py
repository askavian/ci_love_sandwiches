# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread                                                      #  imports entire google spreadsheet
from google.oauth2.service_account import Credentials               #  imports only credentials functions 
#from pprint import pprint                                          #  Displays pprint statement for better examining lists

SCOPE = [                                                           #  is selected in the API Library on Google API & Services page
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')         #  links to .json file where API Acces credentials is stored
SCOPED_CREDS = CREDS.with_scopes(SCOPE)                             #  calls the defined scope -> see above
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)                    #  checks the credentials against Google API AIM Service
SHEET = GSPREAD_CLIENT.open('ci_love_sandwiches')                   #  loads the spreadsheet if API AIM validation is successfull

#sales = SHEET.worksheet('sales')                                   #  TEST: if API is working
#data = sales.get_all_values()                                      #  TEST: if API is working
#print(data)                                                        #  TEST: if API is working

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:                                                     #  keeps running until data proved is valid
        print("Please enter the sales data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")                       #  "\n" = New Line Character
        data_str = input("Enter your data here: ")                  #  input MUST BE exactly 6 Int
#        print(f"The data provided is {data_str}")                  #  TEST: "f" string for interpolation of values 
        sales_data = data_str.split(",")                            #  REMOVES string-"," and ADDS list-"," creates "data_str" list
        validate_data(sales_data)                                   #  calls "validate_data" function from inside "get_sales_data" function
        if validate_data(sales_data): 
            print("Data is valid!")                                 #  TEST: if while loop is exited
            break                                                   #  breaks the while loop if False
    return sales_data                                               #  returns proccessesed sales_data


def validate_data(values):                                          #  validates data function ("values" is relative to where function is called from)
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
#    print(values)                                                  #  TEST: for raw values input
    try:
        [int(value) for value in values]                            #  converts all values in list to integer
        if len(values) != 6:                                        #  if the values (list) IS NOT exactly 6 numbers     
            raise ValueError(                                       #  raises ValueError and shows lenght given            
                f"Exactly 6 values required, you provided {len(values)}"
            ) 
    except ValueError as e:                                         #  "e" is Python shorthand for ERROR    
        print(f"Invalid data: {e}, please try again.\n")            #  combines "raise ValueError" into statement wie "e" keyword                 
        return False                                                #  returns False if ValueError was raised
    return True                                                     #  returns True if validation is corret


#def update_sales_worksheet(data):                                  #  pushes sales data to google sheet after validation
#    """
#    Update sales worksheet, add new row with the list data provided
#    """
#    print("Updating sales worksheet...\n")
#    sales_worksheet = SHEET.worksheet("sales")                     #  targets "sales" page in google sheet
#    sales_worksheet.append_row(data)                               #  adds data as a new row 
#    print("Sales worksheet updated successfully.\n")


#def update_surplus_worksheet(new_surplus_data):                    #  pushes surplus data to google sheet after validation
#    """
#    Update surplus worksheet, add new row with the list data provided
#    """
#    print("Updating surplus worksheet...\n")
#    worksheet_to_update = SHEET.worksheet(worksheet)               #  targets "surplus" page in google sheet
#    worksheet_to_update.append_row(data)                           #  adds data as a new row 
#    print("Surplus worksheet updated successfully.\n")


def update_worksheet(data, worksheet):                              #  GENERAL FUNCTION AFTER REFACTORING TO MERGE BOTH UPDATE FUNCTIONS TO ONE
    """
    GENERAL FUNCTION
    Recieves a list of integers to be inserted into a worksheet.
    Update the relevant worksheet with the data provided.
    """
    print(f"Updating {worksheet} worksheet...\n")                   #  Uses "f" argument to insert what is been updated
    sales_worksheet = SHEET.worksheet(worksheet)                    #  targets any worksheet page that is givin
    sales_worksheet.append_row(data)                                #  adds data as a new row 
    print(f"{worksheet} worksheet updated successfully.\n")


def caluclate_surplus_data(sales_row):                              #  Substracts sales figures from stock
    """
    Compare sales with stock and calculate the surplus for each type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste.
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
#    pprint(stock)                                                  #  TEST: pprint for accurate list print
    stock_row = stock[-1]                                           #  List Index [-1] only gets last row from list / len method also possible
#    print(f"stock row: {stock_row}")                               #  TEST: print for showing if [-1] works correctly
#    print(f"sales row: {sales_row}")                               #  TEST: print for showing sales data is still correct
    surplus_data = []                                               #  VAR for surplus data
    for stock, sales in zip(stock_row, sales_row):                  #  for loop with ZIP Method for calculating multiple lists 
        surplus = int(stock) - sales                                #  Converts to INT and is calculating Surplus
        surplus_data.append(surplus)                                #  Adds data as new row ???
#    print(surplus_data)                                            #  TEST: to see if surplus calculation is correct
    return surplus_data                                             #  Returns surplus_data and stores it in surplus_data above


def get_last_5_entries_sales():
    """
    Collects collumns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists
    """
    sales = SHEET.worksheet("sales")
    columns = []                                                    #  creates new list that contains all product's last five entries
    for ind in range(1, 7):                                         #  1 is Start from and 7 is where the range ends (cuts out 0)
#        print(ind)                                                 #  TEST: functionallity of for loop
        column = sales.col_values(ind)                              #  Applies ind numbers to columns 
        columns.append(column[-5:])                                 #  list slicing for only the last 5 items
#    pprint(columns)                                                #  TEST: pprints all columns imported / ":"" for slicing multiple values
    return columns                                                  #  Returns calculation als variable columns


def calculate_stock_data(data):       
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []                                             #  list is filled by this calculation
    for column in data:
        int_column = [int(num) for num in column]                   #  converts all entries to INT
        average = sum(int_column) / len(int_column)                 #  average (sum of a column) / length
#        average = sum(int_column) / 5                              #  ALTERNATIVE method because length is always 5 here
        stock_num = average * 1.1                                   #  adds 10% to average
        new_stock_data.append(round(stock_num))                     #  appends the list with new line and values / rounds it to whole numbers
#    print(new_stock_data)                                          #  TEST: prints rounded 110% calculated data
    return new_stock_data                                           #  Returns calculation als variable columns


def main():                                                         #  Common practise to call every function step by step in one place
    """
    Run all programm functions
    """
    data = get_sales_data()                                         #  stores sales data after validation in new var "data"
#    print(data)                                                    #  TEST: prints validated and final sales data input
    sales_data = [int(num) for num in data]                         #  converts and stores all list entries to integer
#    print(sales_data)                                              #  TEST: prints validated and final sales data input
#    update_sales_worksheet(sales_data)                             #  calls function for pushing data to sheet SALES ONLY FUNCTION
    update_worksheet(sales_data, "sales")                           #  calls function for pushing data to sheet GENERAL FUNCTION
    new_surplus_data = caluclate_surplus_data(sales_data)           #  VAR and call for function
#    print(new_surplus_data)                                        #  TEST: Prints Surplus data after calculatiing before commiting
#    update_surplus_worksheet(new_surplus_data)                     #  calls update surplus function with calculated data from above SURPLUF FUNCTION LNY
    update_worksheet(new_surplus_data, "surplus")                   #  calls update surplus function with calculated data from above GENERAL FUNCTION
    sales_columns = get_last_5_entries_sales()                      #  calls function for last 5 sales data entries (sorts it)
    stock_data = calculate_stock_data(sales_columns)                #  calls for function to take last 5 sales data (average + 10%)
#    print(stock_data)                                              #  TEST: prints 110% stock average for forecasting
    update_worksheet(stock_data, "stock")                           #  calls UPDATE stock_data function from above GENERAL FUNCTION

print("Welcome to Love Sandwiches Data Automation \n")              #  First thing to be displayed before the function main()
main()                                                              #  Function always needs to be called BELOW from it's position
                              