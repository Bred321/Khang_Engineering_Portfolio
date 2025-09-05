import os
from playwright.sync_api import sync_playwright
from capture_image import run
from create_image_path import create_image_link
import logging


def extract_iv_curves(result_dict, case_path, find_pins, output_path):
    """
    Take screenshot of the IV curve of an input pin name and store in a directory
    :param output_path: the path to store the output files
    :param case_path: the path leading to the .html result
    :param find_pins: contain the pins failing for the input failure type
    :param result_dict: contains the unit VID and its link to the VIRAL result website
    :return: None
    """

    # Extract the case name
    case_split = case_path.split('\\')
    case_name = case_split[:][-1]

    # Create a folder for each case
    if output_path != '':
        case_folder = output_path + f'\\{case_name}-IV Curves Images'
    else:
        case_folder = case_path + f'\\{case_name}-IV Curves Images'

    try:
        os.makedirs(case_folder, exist_ok=True)
    except Exception as e:
        logging.error("The file has already existed or there are some errors related to file creation issue.")

    # Create a sub folder for each pin in a case
    for pin in find_pins:
        print(f"Working on pin {pin} ")

        # Create a new folder path in the directory to store the images
        if output_path != '':
            sub_folder_path = case_folder + f'\\{case_name}-IV of pin ' + pin
        elif output_path == '':
            sub_folder_path = case_folder + f'\\{case_name}-IV of pin ' + pin

        # Create a new folder
        try:
            os.makedirs(sub_folder_path, exist_ok=True)
        except Exception as e:
            logging.error("The file has already existed or there are some errors related to file creation issue.")

        # Loop through each unit VID and its path in the dictionary
        # for vid_num, vid_path in result_dict.items():
        #     try:
        #         image_link = create_image_link(vid_path, pin)
        #         with sync_playwright() as p:
        #             run(p, image_link, vid_num, sub_folder_path, pin)
        #     except Exception as e:
        #         logging.error('Images capturing problems')

        try:
            for vid_num, vid_path in result_dict.items():
                image_link = create_image_link(vid_path, pin)
                run(image_link, vid_num, sub_folder_path, pin)
        except Exception as e:
            logging.error('Images capturing problems')


