import csv

# global variables
CSV_FILE_ADDRESS = 'success_users.csv'


def print_date(success_logged_in):
    global CSV_FILE_ADDRESS

    with open(CSV_FILE_ADDRESS, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for item in success_logged_in:
            writer.writerow(item)
