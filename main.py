"""
This Python script takes a directory path and an optional number of processes as command-line arguments.
It retrieves a list of files from the specified directory, sorts them based on their sizes in descending order,
and initializes a process pool. The goal is to minimize processing skew by distributing the files among the
specified number of processes. The script then iterates through the sorted list of files, assigning batches of
files to the process pool for parallel processing. Each process reads and processes its assigned files concurrently.
The script uses the multiprocessing module to achieve parallelism, aiming to efficiently handle a potentially
large number of files while minimizing the overall processing time.
"""


import sys
from os import listdir
from os.path import isfile, join, getsize
from multiprocessing import Pool


# Get the files from the directory and sort them according to their sizes in descending order.
def get_sorted_file_paths(dir_path):
    file_list = []

    try:
        file_list = listdir(dir_path)
    except FileNotFoundError:
        print('Directory does not exist.')

    file_paths = [join(dir_path, f) for f in file_list if isfile(join(dir_path, f))]
    return sorted(file_paths, key=lambda x: getsize(x), reverse=True)


# Dummy function for reading/processing files
def read_file(file_path):
    with open(file_path, 'r') as file:
        [i.strip().split() for i in file.readlines()]
    print("Processing file: ", file_path)


# Creates a process pool and allocates files to processes
def initialize_processes(file_paths, num_processes):
    # Creates a process pool with the number of processes.
    p = Pool(num_processes)

    # Distributes files based on their sizes to minimize processing skew
    for index in range(0, len(file_paths), num_processes):
        processes = file_paths[:num_processes]
        p.map(read_file, processes)
        file_paths = file_paths[num_processes:]

    p.close()
    p.join()


if __name__ == '__main__':
    dir_path = str(sys.argv[1])
    num_processes = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    file_paths = get_sorted_file_paths(dir_path)
    initialize_processes(file_paths, num_processes)
