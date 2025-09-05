import pandas as pd
import os
import re
import numpy as np
from navigate_ate_result_path import navigating_to_ate_result_path

def analyzing_ate_result(binning_list, class_results, tp_name):
    # Return a dictionary of {"bin number": "interpretation"}
    bin_desripction_list = []
    # Current TP Name: RPLS8H6C2H72D57S043
    # Searching "H72D57S043"
    # result_path = r'\\ger.corp.intel.com\ec\proj\mdl\ha\intel\hdmxprogs\rpl\RPLXXXXCXH72D57S043\TPL'
    # # bin_file_path = r''
    # \\172.19.249.123\LabData\FACR\FACR ATE-PPV\RPL-S881 BGA\CI2419-6940\U3B3120103974

    # Find the bindef file in the TP directory
    bin_file_path = navigating_to_ate_result_path(tp_name)

    if not bin_file_path:
        for bin in binning_list:
            bin_desripction_list.append('No bin description found')
        return bin_desripction_list


    # Read the file and find the bin explanation
    with open(str(bin_file_path), 'r') as bin_read:
        # Read all the lines of the file
        file_text = bin_read.readlines()

        # Match the bin name with the bin description in the file
        try:
            pos = 0
            # Loop through each failing bin
            for bin in binning_list:
                # Find the desciption of the ATE failing pin
                if bin != '0' and class_results[pos] == 'Fail' and bin_file_path:
                    for row in file_text:
                        if bin in row:
                            bin_desripction_list.append(row.strip().replace('\t', '')) 
                            break
                        if row == file_text[-1] and bin not in row:
                             bin_desripction_list.append('Cannot find the bin description')
                # Label the description as 'N/A' if the unit does not have the ATE result
                elif bin == '0' or bin == '' or not bin_file_path:
                    bin_desripction_list.append('N/A')
                # Label the description as 'Pass' and the unit passed the ATE test
                elif class_results[pos] == 'Pass':
                    bin_desripction_list.append('Pass')
                else:
                    bin_desripction_list.append('No information available')
                pos += 1
        except:
            return "Cannot find the bin in the Bin Definition file."
    
    # Converting the list of bin description to Pandas Series data types
    bin_desripction_series = pd.Series(bin_desripction_list)
    # Change all the items of the pin description Series to the string type
    bin_desripction_series = bin_desripction_series.astype('string')

    # Return the binning description Pandas Series
    return bin_desripction_series


# if __name__ == '__main__':
#     analyzing_ate_result()
