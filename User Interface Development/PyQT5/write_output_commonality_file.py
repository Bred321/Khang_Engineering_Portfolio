import datetime
from create_failure_pins_table import creating_failure_pins_table
from create_commonality_table import creating_commonality_table
import os
import logging


def writing_output_commonality_file(case_name, commonality_pins_dict,
                                    pin_package_lists, output_path,
                                    overwrite_confirmed, search_fail,
                                    vid_fail_pins_dict, vid_pin_name_pin_package_dict,
                                    sort_pin_appearance_dict):
    """
    Write the commonality analysis results to a text file in an organized format
    :type pin_package_lists: object
    :param vid_pin_name_pin_package_dict: a dictionary containing the fail pins of each unit
    :param vid_fail_pins_dict: a dictionary containing the fail pins of each unit
    :param search_fail: the failure type
    :param case_name: the input case name
    :param commonality_pins_dict: a list of commonality pins of a specific failure type
    :param pin_package_lists: a list of all the pins in a unit
    :param output_path: the path to store the result text file
    :param overwrite_confirmed: confirm whether overwrite the previous data or not
    """

    output_path = os.path.join(output_path, f'{case_name}_commonality_analysis_result.txt')
    # If the user wants to overwrite the previous data
    writing_mode = 'w' if overwrite_confirmed == "Yes" else 'a'

    # Writing the contents to a file
    with open(output_path, writing_mode) as f:
        # Print the time when the program is executed
        f.write(f'Case name: {case_name}\n')
        f.write(f'---PROGRAM EXECUTION TIMELINE: {datetime.datetime.now()}---\n')
        f.write(f"\n--{search_fail.upper()} PINS TABLE--\n")
        f.write("** Pin name format: Pin Name_[Package Net List]\n")

        # Output a table to summarize the failed pins list for each unit
        vid_fail_pin_table = creating_failure_pins_table(vid_pin_name_pin_package_dict)
        f.write(str(vid_fail_pin_table))
        f.write('\n\n')

        # Output a commonality table
        f.write("\n--COMMONALITY TABLE--\n")
        commonality_table = creating_commonality_table(sort_pin_appearance_dict, pin_package_lists)
        f.write(str(commonality_table))

        # Organize and write the contents to the file
        f.write("\n\n--COMMONALITY PINS SUGGESTION--\n")
        pin_order = 1
        for partial_pin, fail_vids in commonality_pins_dict.items():
            for pin_package_list in pin_package_lists:
                if partial_pin == pin_package_list[1]:
                    f.write(f'{pin_order})\n')
                    f.write(f'Pin Name: {pin_package_list[1]}\n')
                    f.write(f'Units VID failed at this pin ({len(fail_vids)} failed units): {fail_vids}\n')
                    f.write(f'Functional Block: {pin_package_list[2]}\n')
                    f.write(f'UUT Signal Name: {pin_package_list[3]}\n')
                    f.write(f'Package Net List: {pin_package_list[4]}\n\n')
                    pin_order += 1

        f.write(f"\n\n\n\n")

