# Parallel File Processing Script

This Python script takes a directory path and an optional number of threads as command-line arguments.
It retrieves a list of files from the specified directory, sorts them based on their sizes in descending order.
Each thread continually receives files, aiming to distribute workload evenly based on skew values. Skew is calculated
using a formula considering the difference between a thread's processed data and the average, normalized by the maximum
processed data. Threads operate concurrently, dynamically handling new files to minimize imbalances. Global variables
and a lock ensure safe data sharing. The algorithm prints each thread's processed files upon completion.

The goal is to minimize processing skew by distributing the files among the
specified number of threads. The script uses the threading module to achieve parallelism,
aiming to efficiently handle a potentially large number of files while minimizing the overall processing time.
## Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/hilal-demir/ParallelFileProcessing.git
   cd parallel-file-processing

2. **Run the Script:**
   ```bash
    python3 main.py /path/to/your/directory [num_processes]
   
* /path/to/your/directory: Specify the path to the directory containing the files.
* [num_processes] (optional): Specify the number of processes for parallel processing. Default is 10 if not provided.

3. **Project Structure:**
* main.py: The main script containing the file processing logic.

4. **Notes:**
* If the specified directory does not exist, the script will print an error message.
* Error handling is included to capture exceptions during file processing.
