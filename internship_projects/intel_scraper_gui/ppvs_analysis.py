import os
import pandas as pd


def find_ppvs_file(unit_ppv_path):
    # FUNCTION: find the PPVM file in the directory path
    # print("Checking PPV Path: ", os.listdir(unit_ppv_path))
    result_file = ''
    for file in os.listdir(unit_ppv_path):
        # Return the PPVM file (the file with trailing 95)
        if '7297' in file or '7899' in file:
            result_file = file
            if 'PASS' in file:
                return 'Pass'
        elif (file == os.listdir(unit_ppv_path)[-1]) and ('7297' in file or '7899' in file):
            return 'N/A'
    # Return 'N/A' if no PPVM result folder is found.
    return result_file


def read_the_ppvs_file(file, ppvs_vid_bin):
    # FUNCTION: read the file and print out the failure bin description
    detected_bin = []
    # Return the failure pin
    with open(file, 'r') as f:
        # Reading through each line in a file
        lines = f.readlines()
        line_list = iter(lines)
        for line in line_list:
            # Navigate to the 'Bins in this run' section
            if 'Bins in this run' in line:
                line = next(line_list)
                # Record the failure description and store in the list
                while '=========' not in line.strip():
                    # Add the bin description to the list
                    detected_bin.append(line.strip().split()[-1][2:])
                    # Move to the next line
                    line = next(line_list)

        # Return the bin description list   
        return detected_bin

def analyse_ppvs_paths(vid_list, ppv_path, ppvs_vid_bins_series):
    # ppvm_bins_series = pd.Series()
    ppvs_bins_list = []
    ppvs_bins_series = []
    # print("Checking PPV Path: ", os.listdir(ppv_path))
    for unit_vid in vid_list:
        unit_ppv_path = os.path.join(ppv_path, unit_vid)

        if not os.path.exists(unit_ppv_path):
            ppvs_bins_series.append(['N/A'])
            continue
            # continue

        if ppvs_vid_bins_series[unit_vid] == '0':
            ppvs_bins_series.append(['N/A'])
            continue
        
        # Navigating the the files containing '7297' or '7899' in the name
        ppvs_file = find_ppvs_file(unit_ppv_path)
        if ppvs_file == 'N/A':
            ppvs_bins_series.append(['N/A'])
            continue

        if ppvs_file == 'Pass':
            ppvs_bins_series.append(['Pass'])
            continue

        # Looping through '7297' and '7899' files
        unit_ppvs_folder = os.path.join(unit_ppv_path, ppvs_file)
        # Looping through the sub-files inside the folder
        for file in os.listdir(unit_ppvs_folder):
            result_file = os.path.join(unit_ppvs_folder, file)
            # Call the function to analyze the result
            failed_bin = read_the_ppvs_file(result_file, ppvs_vid_bins_series[unit_vid])
            ppvs_bins_list.extend(failed_bin)

        # Add the bin description to the list
        ppvs_bins_series.append(',  '.join(ppvs_bins_list))

        # Regresh the bin list
        ppvs_bins_list = []

    ppvs_bins_series = pd.Series(ppvs_bins_series)
    # ppvs_bins_series.to_excel("output_xlsx.xlsx")
    return ppvs_bins_series
