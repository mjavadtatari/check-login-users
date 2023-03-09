import csv

# global variables
CSV_FILE_ADDRESS = 'users.csv'


def export_csv_to_list(csv_file):
    rows_without_headers = []

    with open(csv_file, 'r') as f:
        for item in csv.reader(f):
            rows_without_headers.append(item)

        # column_name = rows_without_headers[0]
        rows_without_headers.pop(0)

    return rows_without_headers


def get_data():
    exported_list = export_csv_to_list(CSV_FILE_ADDRESS)
    return {
        'exported_list': exported_list,
    }
