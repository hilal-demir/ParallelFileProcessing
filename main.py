"""
This Python script takes a directory path and an optional number of threads as command-line arguments.
It retrieves a list of files from the specified directory, sorts them based on their sizes in descending order.
Each thread continually receives files, aiming to distribute workload evenly based on skew values. Skew is calculated
using a formula considering the difference between a thread's processed data and the average, normalized by the maximum
processed data. Threads operate concurrently, dynamically handling new files to minimize imbalances. Global variables
and a lock ensure safe data sharing. The algorithm prints each thread's processed files upon completion.

The goal is to minimize processing skew by distributing the files among the
specified number of threads. The script uses the threading module to achieve parallelism,
aiming to efficiently handle a potentially large number of files while minimizing the overall processing time.
"""


import sys
from os import listdir
from os.path import isfile, join, getsize
from threading import Thread, Lock


# Global variables
file_paths = []
processed_files = []
thread_loads = []
lock = Lock()


# Gets the files from the directory and sorts them according to their sizes in descending order.
def get_sorted_file_paths(dir_path):
    file_list = []

    try:
        file_list = listdir(dir_path)
    except FileNotFoundError:
        print('Directory does not exist.')

    if len(file_list) == 0:
        print('Directory is empty.')
        sys.exit(1)

    files = [join(dir_path, f) for f in file_list if isfile(join(dir_path, f))]
    return sorted(files, key=lambda x: getsize(x), reverse=True)


# Dummy function for reading/processing files
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            [i.strip().split() for i in file.readlines()]
        print("Processing file:", file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except PermissionError:
        print(f"Permission error accessing file: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


# Assigns files to a thread according to the skew value and the thread load
def worker(thread_id):
    global file_paths, processed_files, thread_loads

    while True:
        with lock:
            # Check if there are files to process
            if not file_paths:
                break

            # Find the thread with the minimum skew
            min_skew_thread = min(range(len(thread_loads)), key=lambda i: calculate_skew(i))

            # Assign the file to the thread with the minimum skew and update thread load
            file_path = file_paths.pop(0)
            file_size = getsize(file_path)
            thread_loads[min_skew_thread] += file_size

            # Assign the file to the current thread
            processed_files[min_skew_thread].append(file_path)

        # Process the file
        read_file(file_path)


# Calculates the skew value
def calculate_skew(thread_id):
    avg_amount_processed = sum(thread_loads) / len(thread_loads)
    max_amount_processed = max(thread_loads)

    if max_amount_processed == 0:
        return 0  # Handle the case where all threads have not processed any files yet

    amount_processed_by_thread = thread_loads[thread_id]
    return (amount_processed_by_thread - avg_amount_processed) / max_amount_processed


if __name__ == '__main__':
    dir_path = str(sys.argv[1])
    num_threads = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    file_paths = get_sorted_file_paths(dir_path)

    # Handle the case where there are fewer files in the directory than the number of threads
    if len(file_paths) < num_threads:
        print(f"There are not enough files to fully utilize {num_threads} threads.")
        num_threads = len(file_paths)

    # Initialize global variables for thread information
    processed_files = [[] for _ in range(num_threads)]
    thread_loads = [0] * num_threads

    # Create and start threads
    threads = [Thread(target=worker, args=(i,)) for i in range(num_threads)]
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Print the files processed by each thread
    for i, files in enumerate(processed_files):
        print(f"Thread {i} processed the following files:")
        for file_path in files:
            print(file_path)
