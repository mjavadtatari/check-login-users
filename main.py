# This is a sample Python script.
import os

import get_data_from_csv
import check_login


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import set_data_to_csv


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def print_bye():
    # Use a breakpoint in the code line below to debug your script.
    print('Program Executed Successfully')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi(os.getlogin())

    USERS_DATA = get_data_from_csv.get_data()['exported_list']
    success_logged_in = check_login.run_module(USERS_DATA)
    set_data_to_csv.print_date(success_logged_in)

    print_bye()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
