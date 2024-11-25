import os
import get_data_from_csv
import check_login
import ibsng_login_check
import concurrent.futures
import set_data_to_csv

WORKERS_NUM = 5


def print_hi(name):
    print(f'Hi, {name}')


def print_bye():
    print('Program Executed Successfully')


def chunk_data(data, num_chunks):
    """Distribute data into roughly equal-sized chunks."""
    chunk_size = len(data) // num_chunks
    remainder = len(data) % num_chunks

    start = 0
    for i in range(num_chunks):
        # Add 1 extra item to the first 'remainder' chunks
        extra = 1 if i < remainder else 0
        end = start + chunk_size + extra
        yield data[start:end]
        start = end


if __name__ == '__main__':
    print_hi(os.getlogin())

    USERS_DATA = get_data_from_csv.get_data()['exported_list']

    # Divide into 5 roughly equal chunks
    user_batches = list(chunk_data(USERS_DATA, WORKERS_NUM))

    # Process the batches concurrently
    success_logged_in_all = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS_NUM) as executor:
        futures = [executor.submit(ibsng_login_check.run_module, batch)
                   for batch in user_batches]

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                success_logged_in_all.extend(result)
            except Exception as e:
                print(f"Error processing batch: {e}")

    # success_logged_in = check_login.run_module(USERS_DATA)
    # success_logged_in = ibsng_login_check.run_module(USERS_DATA)
    # set_data_to_csv.print_date(success_logged_in)
    set_data_to_csv.print_date(success_logged_in_all)

    print_bye()
