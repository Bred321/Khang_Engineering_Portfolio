'''
    Summary:
    This Python script will enter an finite loop
    where data about CPU usage, memory usage, 
    disk usage, etherther throughput will
    be logged to a csv file.

    Inputs:
    - The maximum number of file in the result folder
    - The time to begin logging to a new .csv file
    - The data logging frequency

    Functions:
    - input_validation: to validate the user's inputs
    - preprocess_folder: to delete the oldest files before logging
    - create_and_preprocess_folder: create a new logging folder if not existing,
                                    otherwise preprocess the folder
    - delete_file: delete the oldest files
    - get_network_speed: calculate the network throughput
    - get_network_data: get throughput of the network interfaces 
    - write_data: to write values to a csv file
    - execute_main_operation: monitor the whole data logging process
'''
# Import the libraries
import time
from datetime import date
import csv
import os
import psutil


def input_validation(mode):
    '''Validate if the user has entered a valid number

    Args:
        mode (string): Specifies which parameter needs to be checked. 
                       Each parameter comes with a unique rules

    Returns:
        in_val (int or float): the valid value that the user has successfully entered'''
    message = ''
    in_val = 0

    # Check rules for the maximum number of files before the program starts deleting
    if mode == 'delete_files':
        message = 'Please enter the maximum number of csv files in a folder (integer > 0): '
        while True:
            try:
                # Get the user input
                in_val = int(input(message))
                # Check if the input is greater than zero
                if in_val > 0:
                    return in_val
                # Raise Error when the input is less than zero
                raise ValueError
            except ValueError:
                print('Error: Please enter an integer greater than zero !!!')

    # Check rules for the duration before the program starts creates a new file
    elif mode == 'create_new_file':
        message = 'Please enter the duration of logging ' \
                  'to the same file (float or integer > 0 in seconds): '
        while True:
            try:
                # Get the user input
                in_val = float(input(message))
                # Check if the input is greater than zero
                if in_val > 0:
                    return in_val
                # Raise Error when the input is less than zero
                raise ValueError
            except ValueError:
                print('Error: Please enter a float or an integer greater than zero !!!')

    # Check rules for the data loggging frequency
    elif mode == 'log_data':
        message = 'Please enter the data logging frequency (float or integer > 0 in seconds): '
        while True:
            try:
                # Get the user input
                in_val = float(input(message))
                # Check if the input is greater than zero
                if in_val > 0:
                    return in_val
                # Raise Error when the input is less than zero
                raise ValueError
            except ValueError:
                print('Error: Please enter a float or an integer greater than zero !!!')
    elif mode == 'read_cpu':
        message = 'Please enter the interval to read CPU usage (float or integer > 0 in seconds): '
        while True:
            try:
                # Get the user input
                in_val = float(input(message))
                # Check if the input is greater than zero
                if in_val > 0:
                    return in_val
                # Raise Error when the input is less than zero
                raise ValueError
            except ValueError:
                print('Error: Please enter a float or an integer greater than zero !!!')
    # Return the valid input value entered by the user
    return in_val

def preprocess_folder(folder_path, files_num_to_begin_deletion):
    '''Count the number of files in the folder. 
    If it exceeds the threshold, delete the oldest files until reaching the desired maximum number

    Args:
        folder_path (string): represents the folder relative path
        files_num_to_begin_deletion (integer): depicts the maximum number of files in the directory 
                                                until the program starts deleting the oldest files

    Returns:
        existing_file_list (list): contains the currently existing file names 
                                   after folder preprocessing'''
    # Return a list of existing files in the existing folder
    existing_file_list = list(os.listdir(folder_path))
    #* If the number of existing files exceeds a pre-configured number,
    #* begin deleting the oldest ones recursively
    #* until the total file number stays lower than the threshold
    while len(existing_file_list) > files_num_to_begin_deletion:
        # Create a delete file path
        delete_file_path = os.path.join(folder_path, existing_file_list[0])
        # Delete the file in the directory if existing
        if os.path.exists(delete_file_path):
            os.remove(delete_file_path)
        # Remove the file name from the existing file list
        del existing_file_list[0]

    # Return a new existing file list after cleaning
    return existing_file_list

def create_and_preprocess_folder(folder_path, files_num_to_begin_deletion):
    '''If the folder has not existed, create a new one. 
        Otherwise, preprocess the existing folder to keep the number of files in control

    Args:
        folder_path (string): represents the path pointing to the directory where the data is stored
        files_num_to_begin_deletion (integer): depicts the maximum number of files in the directory 
                                                until the program starts deleting the oldest files

    Returns:
        files_control_list (list): to keep track of how many files are currently in the folder'''
    #* Check whether the folder exists or not. If not, create a new folder.
    #* If yes, preprocess the folder
    files_control_list = []
    if os.path.exists(folder_path):
        #! Notify the folder has existed. The program will begin processing the folder
        print('The folder exists. Begin preprocessing folder !!')
        # Begin the preprocessing operation
        files_control_list = preprocess_folder(folder_path, files_num_to_begin_deletion)
        #! Notify the folder has been preprocessed
        print('Done preprocessing the folder. Begin operation !!!')
    else:
        #! Notify the program is creating a new folder
        print('Creating a folder')
        os.mkdir(folder_path)
    # Return the tracking list
    return files_control_list

def delete_file(folder_path, file_name):
    '''Delete a file

    Args:
        folder_path (string): represents the path pointing to the directory where the data is stored
        file_name (string): represents the file name

    Returns:
        This function will not return any value'''
    # Define a deleted file path
    delete_file_path = os.path.join(folder_path, file_name)
    # Delete the file in the directory
    if os.path.exists(delete_file_path):
        os.remove(delete_file_path)

def get_network_speed(interface='lo0'):
    '''Calculate the network throughput

    Args:
        interface (str, optional): Specify which network interface to measure. Defaults to 'lo0'.

    Returns:
        througput_list (list): contains the measured throughput of a specified network interface'''
    # Get network stats before
    net1 = psutil.net_io_counters(pernic=True).get(interface, None)
    if net1 is None:
        return ['N/A', 'N/A']
    # Wait for 1 second
    time.sleep(1)
    # Get network stats after 1 second
    net2 = psutil.net_io_counters(pernic=True)[interface]
    # Calculate speeds in Kbps
    send_kbps = (net2.bytes_sent - net1.bytes_sent) * 8 / 1000
    recv_kbps = (net2.bytes_recv - net1.bytes_recv) * 8 / 1000
    througput_list = [send_kbps, recv_kbps]
    # Return the throughput results in the list form
    return througput_list

def get_network_data():
    '''Get the throughput of the network interfaces

    Returns:
        network_data_list (list): contains the throughput result of each network interface'''
    network_data_list = []
    # Collect data from em0 to em6
    for i in range(0, 7):
        em_interface = 'em' + str(i)
        em_throughput_list = get_network_speed(em_interface)
        network_data_list.append(em_throughput_list)
    # Collect data from lagg0 to lagg1
    for i in range(0, 2):
        lagg_interface = 'lagg' + str(i)
        lagg_throughput_list = get_network_speed(lagg_interface)
        network_data_list.append(lagg_throughput_list)
    return network_data_list

def write_data(csv_file, time_to_create_new_file, data_log_frequency,  cpu_reading_interval):
    '''Get the resources reading and write them to a CSV file

    Args:
        csv_file (string): _description_
        time_to_create_new_file (integer): _description_
        data_log_frequency (integer): _description_

    Returns:
        This function will not return any value'''
    # Create a writer engine for a csv file
    writer = csv.writer(csv_file)
    # Define the headers titles
    headers = ['Date', 'Time', 'CPU_Usage_Percent',
               'Memory_Usage_Percent', 'Disk_Usage_Percent',
               'em0_Sending_Kbps_Speed', 'em0_Receiving_Kbps_Speed',
               'em1_Sending_Kbps_Speed', 'em1_Receiving_Kbps_Speed',
               'em2_Sending_Kbps_Speed', 'em2_Receiving_Kbps_Speed',
               'em3_Sending_Kbps_Speed', 'em3_Receiving_Kbps_Speed',
               'em4_Sending_Kbps_Speed', 'em4_Receiving_Kbps_Speed',
               'em5_Sending_Kbps_Speed', 'em5_Receiving_Kbps_Speed',
               'em6_Sending_Kbps_Speed', 'em6_Receiving_Kbps_Speed',
               'lagg0_Sending_Kbps_Speed', 'lagg0_Receiving_Kbps_Speed',
               'lagg1_Sending_Kbps_Speed', 'lagg1_Receiving_Kbps_Speed',]
    # Write the header titles to the Excel file
    writer.writerow(headers)
    # Get the current time to start counting and calculating to
    # see if it reaches time_to_create_new_file
    start_time = time.time()
    # Enter an infinite loop which breaks after a specified amount time
    # defined in the 'time_to_create_new_file' variable
    while True:
        # Get date
        current_date = date.today()
        # Get current time
        current_time = time.strftime('%H:%M:%S%z', time.localtime())
        # Get CPU usage data
        cpu_percent = f'{psutil.cpu_percent(interval= cpu_reading_interval):.4f}%'
        #Get memory usage data
        memory_usage = f'{psutil.virtual_memory().percent:.4f}%'
        # Get disk usage
        disk_usage = f'{psutil.disk_usage("/").percent:.4f}%'
        # Get network data
        network_data = get_network_data()
        # Write the data to the csv file
        writer.writerow([current_date, current_time, cpu_percent,
                         memory_usage, disk_usage,
                         network_data[0][0], network_data[0][1], #em0
                         network_data[1][0], network_data[1][1], #em1
                         network_data[2][0], network_data[2][1], #em2
                         network_data[3][0], network_data[3][1], #em3
                         network_data[4][0], network_data[4][1], #em4
                         network_data[5][0], network_data[5][1], #em5
                         network_data[6][0], network_data[6][1], #em6
                         network_data[7][0], network_data[7][1], #lagg0
                         network_data[8][0], network_data[8][1]  #lagg1
                        ])
        # Measure the current time to calculate the elapsed amount of time
        end_time = time.time()
        # Measure the elasped time
        elapsed_time = end_time - start_time
        # If the amount of passed time excess the time_to_create_new_file,
        # break out the infinite loop
        if elapsed_time > time_to_create_new_file:
            break
        # Sleep for a pre-configured duration
        time.sleep(data_log_frequency)

def execute_main_operation(folder_name,
                            files_control_list,
                            files_num_to_begin_deletion,
                            time_to_create_new_file,
                            data_log_frequency,
                            cpu_reading_interval):
    '''Execute the overall operation of the program

    Args:
        folder_name (string): represents the folder name
        files_control_list (list): _description_
        files_num_to_begin_deletion (integer): depicts the maximum number of files 
                                               until the program starts deleting the oldes ones
        time_to_create_new_file (integer): depicts the amount of time 
                                           until the program starts writing data to a new file
        data_log_frequency (integer): depicts data logging frequency
                                      (how frequeny should the program read resources data?)

    Returns:
        This function will not return any value'''
    #! Notify the program starts running
    print('The program is running...')
    #* Enter an infitnite loop
    while True:
        # If the number of files exceeds the preconfigured number, delete the oldest file
        if len(files_control_list) >= files_num_to_begin_deletion:
            delete_file(folder_name, files_control_list[0])
            del files_control_list[0]
        # Create the file name
        current_time = time.strftime('%H(h)_%M(min)_%S(sec)', time.localtime())
        current_date = date.today()
        file_num = f'Logging_Resources_Date_{current_date}_Time_{current_time}'
        file_name = file_num + '.csv'
        # Add the file name to the tracking list to keep track of the number of files in the folder
        files_control_list.append(file_name)
        #! Notify the program is writing to a file
        print(f'Writing to the file: \'{file_name}\' ...')
        # Construct a file path
        file_path = os.path.join(folder_name, file_name)
        # Write data to the file
        with open(file_path , 'a', encoding='utf-8') as f:
            write_data(f, time_to_create_new_file, data_log_frequency, cpu_reading_interval)
        #! Notify the program has done writing to the file
        print(f'Complete the file: \'{file_name}\'')


#! -- MAIN PROGRAM --
if __name__ == '__main__':
    #* Configurable parameters
    print('--- PARAMETER CONFIGURATION BEGINS---')
    files_num_to_begin_deletion_in = input_validation(mode='delete_files')
    time_to_create_new_file_in = input_validation(mode='create_new_file')
    data_log_frequency_in  = input_validation(mode='log_data')
    cpu_reading_interval_in = input_validation(mode='read_cpu')
    print('--- PARAMETER CONFIGURATION ENDS---')
    #* Print out the input parameters for tracking
    print('-----------------------------------')
    print('--SCRIPT CONFIGURATION--')
    print(f'Maximum number of csv files in a folder: {files_num_to_begin_deletion_in} (files)')
    print(f'Duration of logging to the same file: {time_to_create_new_file_in} (sec)')
    print(f'Data logging frequency: {data_log_frequency_in} (sec)')
    print(f'CPU reading interval: {cpu_reading_interval_in} (sec)')
    print('-----------------------------------')
    print('--PROGRAM STARTS--')
    #* Operation parameters (not configurable)
    # Define the folder name
    FOLDER_NAME = 'resources_logging'
    # Define a list to monitor the existent file names
    files_control = []
    #* Preprocess the folder where data is stored
    # Create a new if not existing and preprocess that folder
    try:
        files_control = create_and_preprocess_folder(FOLDER_NAME, files_num_to_begin_deletion_in)
    except Exception as e:
        #! Notify the error to the user
        print(f'An error has occured: {e}')
    #* Begin the main execution
    try:
        execute_main_operation(FOLDER_NAME,
                               files_control,
                               files_num_to_begin_deletion_in,
                               time_to_create_new_file_in,
                               data_log_frequency_in,
                               cpu_reading_interval_in)
    except KeyboardInterrupt:
        #! Notify the program has stopped running
        print('Program terminated !!!')
    except Exception as e:
        #! Notify the error to the user
        print(f'An error has occured: {e}')
