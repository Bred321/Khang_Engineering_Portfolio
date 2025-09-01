from prettytable import PrettyTable


def creating_failure_pins_table(vid_pin_name_pin_package_dict):
    """
    Create a table with all the failed pins for each unit
    :param vid_pin_name_pin_package_dict:  contains the unit VID and its respective fail pins
    :return: a table object from the prettytable module
    """

    # Find the pin list with the greatest length
    max_list_length = 0
    for a_list in list(vid_pin_name_pin_package_dict.values()):
        if len(a_list) > max_list_length:
            max_list_length = len(a_list)


    # Horizontal solution
    vid_fail_pin_table = PrettyTable(["Unit VIDs", "Failed pins"])
    vid_fail_pin_table._max_width = {"Unit VIDs": 20, "Failed pins": 150}

    for unit_vid, pin_list in vid_pin_name_pin_package_dict.items():
        vid_fail_pin_table.add_row([unit_vid, ', '.join(pin_list)])
        vid_fail_pin_table.add_row(['', ''])
        vid_fail_pin_table.add_row(['---------', '-------------------------------------------------------------------'])
        vid_fail_pin_table.add_row(['', ''])

    # Return the table
    return vid_fail_pin_table
