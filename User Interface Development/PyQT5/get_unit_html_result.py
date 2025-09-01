import os
import webbrowser as wb
import shutil
from check_if_act_fail import checking_if_act_fail


def get_unit_html(path, case_name, open_in_html_confirmed, output_path, copy_file_confirmed):
    """
    Fetch the link leading to the ACT result of the unit. Optionally open that link directly or copy the result folder
    to the user-input folder
    :param path: the link leading to the case folder
    :param case_name: the name of the input case
    :param open_in_html_confirmed: a boolean
    :param output_path: the user-defined storing location
    :param copy_file_confirmed: a boolean to perform the file copying and moving actions
    :return: dictionary consisting of each unit VID and its corresponding .html link
    """

    # Create a dictionary with the following information {'VID' : 'result.html '}
    result_dict = {}

    # List all the files of the folder of a case
    files = os.listdir(os.path.normpath(path))

    # Looping through each file
    for file in files:
        if file.startswith('Html_'):
            # Create the file path with the unit folder
            # Get access to the sub folder
            # file_path = os.path.join(path, file)
            file_path = path + f"\\{file}"
            # Open the unit folder
            # Create the path guiding to the html file of that unit
            # result_path = os.path.join(file_path, 'result.html')
            result_path = file_path + "\\result.html"

            # Raise an exception if a path does not exist
            if os.path.exists(path):
                did_fail = checking_if_act_fail(result_path)
                if not did_fail:
                    unit_vid = file.split('_')[1]
                    result_dict[unit_vid] = result_path

                    # Copy the result files to the specified location if confirmed
                    if copy_file_confirmed == 'Yes':
                        # Copy the html result and move to the desired folder
                        modified_des_path = os.path.join(output_path, f'{case_name}_{file.split('_')[1]}_ACT_Result')
                        shutil.copytree(file_path, modified_des_path, dirs_exist_ok=True)
            else:
                raise Exception("Sorry, the result path does not exist in the system. Please try again")

    if open_in_html_confirmed == "Yes":
        for link in result_dict.values():
            wb.open(link)

    return result_dict
