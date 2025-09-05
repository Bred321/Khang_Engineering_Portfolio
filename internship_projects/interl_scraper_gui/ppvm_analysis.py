import os
import pandas as pd


def find_ppvm_file(unit_ppv_path):
    # FUNCTION: find the PPVM file in the directory path
    # print("Checking PPV Path: ", os.listdir(unit_ppv_path))
    for file in os.listdir(unit_ppv_path):
        # Return the PPVM file (the file with trailing 95)
        if '7295' in file:
            return file
    # Return 'N/A' if no PPVM result folder is found.
    return 'N/A'


def read_the_ppvm_file(file):
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
                    # print(line.strip().split()[-1])
                    detected_bin.append(line.strip().split()[-1][2:])
                    # print(line.strip().split()[-1])
                    line = next(line_list)

        # Return the bin description list   
        return detected_bin


def analyse_ppvm_paths(vid_list, ppv_path):
    # ppvm_bins_series = pd.Series()
    ppvm_bins_list = []
    ppvm_bins_series = []
    # print("Checking PPV Path: ", os.listdir(ppv_path))
    for unit_vid in vid_list:
        unit_ppv_path = os.path.join(ppv_path, unit_vid)
        if not os.path.exists(unit_ppv_path):
            ppvm_bins_series.append(['N/A'])
            # continue
        else:
            ppvm_file = find_ppvm_file(unit_ppv_path)
            if not ppvm_file:
                return 
            # If the PPVM has the "Pass" result
            if 'PASS' in ppvm_file:
                ppvm_bins_series.append(['Pass'])
            else:
                # Find the bin description if the PPVM does not pass
                unit_ppvm_folder = os.path.join(unit_ppv_path, ppvm_file)
                for file in os.listdir(unit_ppvm_folder):
                    result_file = os.path.join(unit_ppvm_folder, file)
                    failed_bin = read_the_ppvm_file(result_file)
                    ppvm_bins_list.extend(failed_bin)
                ppvm_bins_series.append(',  '.join(ppvm_bins_list))
            ppvm_bins_list = []

    ppvm_bins_series = pd.Series(ppvm_bins_series)
    # ppvm_bins_series.to_excel("output_xlsx.xlsx")
    return ppvm_bins_series


# if __name__ == '__main__':
#     # unit_vid_list = ['U3QL740202237']
#     unit_vid_list = ['U3QL740202237','U31P3R2603156']
#     ppv_path = 'file://172.19.249.123/LabData/FACR/FACR%20ATE-PPV/RPL-S881%20BGA/CI2416-5956/PPV/'
#     modified_ppv_path = '\\\\' + ppv_path.split('://')[1].replace('/', '\\').replace('%20', ' ')
#     analyse_ppvm_paths(unit_vid_list, modified_ppv_path)