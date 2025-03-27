import gspread
from google.oauth2.service_account import Credentials
import prettytable as pt

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('IT-Survey')

def validate(values):
    """
    Validate the user input and return True if valid, False otherwise.
    """
    try:
        int_value = int(values)
        if 1 <= int_value <= 3:
            return True
        else:
            raise ValueError("Please provide a number between 1 and 3.")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

def get_data_by_user_choice():
    """
    Get user choice
    """
    while True:
         print("Select a domain of interest from the list below:")
         print("1: Most popular technologies")
         print("2: Salary")
         print("3: Databases")
         user_input = input("Select a number from 1 to 3:\n ")
         if validate(user_input):
            choice = int(user_input)
            if choice == 1:
                return 'Most-popular-technologies'
            elif choice == 2:
                return 'Salary'
            elif choice == 3:
                return 'Databases'
         else:
            print("Invalid input, please try again.")

def main():
    sheet_name = get_data_by_user_choice()
    data = SHEET.worksheet(sheet_name).get_all_values()
    table = pt.PrettyTable()
    if data:
        # Add columns to the table based on keys of the first record
        table.field_names = data[0]

        # Add rows to the table
        for row in data[1:]:
            table.add_row(row)
    print(table)

if __name__ == "__main__":
    main()
