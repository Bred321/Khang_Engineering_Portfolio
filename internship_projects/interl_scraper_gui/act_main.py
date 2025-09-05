"""
IV CURVES EXTRACTOR

"""

__author__ = "Duong, Bao Khang"
__email__ = "bao.khang.duong@intel.com"
__version__ = "0.0"
__status__ = "Development"
__date__ = "18 March 2024"

import os
from create_fail_pin_dict import fail_pin_dict
from create_vid_pin_name_pin_package_dict import create_pin_package_list_dict
from extract_case_path import get_case_path
from find_commonality import finding_commonality
from get_case_pins_dict import getting_case_pins_dict
from get_iv_curves import extract_iv_curves
from get_pin_package_list import get_pin_functional_package_list
from get_unit_html_result import get_unit_html
from write_output_commonality_file import writing_output_commonality_file
import logging


def act_main_function(case_names, year,
                           output_format, output_path,
                           search_fail, overwrite_confirmed,
                           captured_pins, open_in_html_confirmed,
                           copy_file_confirmed):
    """
        ----MAIN FUNCTION----
    """
    # Set the output path to store the images
    # Send the message if one of the input fields is still missing

    if not (case_names and year and output_path):
        return "Some input fields are missing, please kindly check your inputs again."

    if output_format == "IV Curve images":
        if not captured_pins:
            return "Please provide input for the Pin Names field."

    # Converting the input pin name text into a list
    logging.basicConfig(level=logging.INFO)
    case_list = [case.strip() for case in case_names.split(",")]

    # Create the result path for each case
    case_paths = []
    for case_name in case_list:
        case_path = get_case_path(case_name, year)
        if not os.path.exists(case_path):
            return "The VIRAL folder of this case cannot be reached. Please check the case name or year inputs."
        case_paths.append(case_path)

    # Create each unit result path for each case
    units_htmls_dictionary_list = []
    case_names = []
    for case_path in case_paths:
        # Navigating to the VIRAL .html file
        case_name = case_path.split('\\')[-1]
        case_names.append(case_name)
        units_htmls_dictionary = get_unit_html(case_path, case_name,
                                               open_in_html_confirmed,
                                               output_path, copy_file_confirmed)
        units_htmls_dictionary_list.append(units_htmls_dictionary)

    print(units_htmls_dictionary_list)
    # End the execution if no unit failed the ACT test

    try:
        logging.info("The program is currently working.")
        position = 0
        # Implement a function to write the output to a file
        if output_format == "IV Curve images":
            try:
                vid_pin_dict = getting_case_pins_dict(case_names, captured_pins)
                # Executing the main logic
                for units_htmls_dictionary in units_htmls_dictionary_list:
                    if vid_pin_dict[case_names[position]][0] is not None:
                        # Call the action function to extract the IV Curves images
                        extract_iv_curves(units_htmls_dictionary, case_paths[position],
                                          vid_pin_dict[case_names[position]], output_path)
                        # def extract_iv_curves(result_dict, case_path, find_pins, output_path):
                    position += 1
            except Exception as e:
                logging.error('Execution Error')
                return "There are some errors related to the captured IV Curves, please kindly check the input again."

            print("The program has captured the IV Curves successfully.")
            # Return the completion message
            return "The program has captured the IV Curves successfully."

        elif output_format == "Commonality analysis text file":
            if not units_htmls_dictionary_list[0]:
                return "All the units in this case passed the ACT test."
            # Executing the main logic
            for units_htmls_dictionary in units_htmls_dictionary_list:
                # Get all the pin names, pin package names, net names for the first unit
                try:
                    pin_package_lists = get_pin_functional_package_list(list(units_htmls_dictionary.values())[0])
                    # Print the html link for each unit in the form of dictionary

                    # vid_fail_pins_dict : dictionary of "unit" : "fail pins"
                    # all_unit_pin_list: a list of fail pins list of each unit
                    all_unit_pin_list, vid_fail_pins_dict = fail_pin_dict(units_htmls_dictionary, search_fail)
                    # Find the commonality pins
                    vid_pin_name_pin_package_dict = create_pin_package_list_dict(pin_package_lists, vid_fail_pins_dict)
                    commonality_pins_dict, sort_pin_appearance_dict = finding_commonality(vid_fail_pins_dict)
                except Exception as e:
                    logging.error("Execution Error")
                    return ("There are some errors related to the Commonality "
                            "analysis execution, please kindly check the input again.")

                try:
                    # Call the action function to output the commonality text file
                    writing_output_commonality_file(case_names[position], commonality_pins_dict,
                                                    pin_package_lists, output_path,
                                                    overwrite_confirmed, search_fail,
                                                    vid_fail_pins_dict, vid_pin_name_pin_package_dict,
                                                    sort_pin_appearance_dict)
                    position += 1
                except Exception as e:
                    logging.error("Output File Generation Error")
                    return ("There are some errors related to the Output Commonality File Generation, "
                            "please kindly check the input again.")

            print("The program has completed ACT Result analysis successfully.\n")
            print("-------------")
            # Return the completion message
            return "The program has completed ACT Result analysis successfully."

    except Exception as e:
        # Print out a message in case any error happens
        return "There are some errors related to the execution, please kindly check the input again."



