# Parallel File Processing Script

This Python script is designed to efficiently process a collection of files in parallel. It takes a directory path and an optional number of processes as command-line arguments, retrieves a list of files from the specified directory, and sorts them based on their sizes in descending order. The script then initializes a process pool to minimize processing skew and efficiently handle a potentially large number of files.

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
