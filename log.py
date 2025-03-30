import os

def write_log(input_text):
    """Writes the input text to a log file in the log folder with an automatically ordered name."""
    log_folder = 'log'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    # Get the list of existing log files and determine the next log file number
    existing_logs = [f for f in os.listdir(log_folder) if f.startswith('log_') and f.endswith('.txt')]
    log_numbers = [int(f.split('_')[1].split('.')[0]) for f in existing_logs]
    next_log_number = max(log_numbers) + 1 if log_numbers else 1
    
    # Create the new log file with the next log number
    log_filename = f'log_{next_log_number}.txt'
    log_filepath = os.path.join(log_folder, log_filename)
    
    # Write the input text to the new log file
    with open(log_filepath, 'w') as log_file:
        log_file.write(input_text)
