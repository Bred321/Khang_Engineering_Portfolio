def create_pin_package_list_dict(pin_package_lists, vid_fail_pins_dict):
    """
    Create a dictionary with keys as VIDs and values as pins and package net lists
    :param pin_package_lists:
    :param vid_fail_pins_dict: a dictionary containing the failed pins for each unit
    :return: a dictionary
    """
    vid_pin_name_pin_package_dict = {}
    for unit_vid, unit_failed_pins in vid_fail_pins_dict.items():
        vid_pin_name_pin_package_dict[unit_vid] = []
        for pin_name in unit_failed_pins:
            for pin_package_item in pin_package_lists:
                if pin_package_item[1] == pin_name:
                    vid_pin_name_pin_package_dict[unit_vid].append(f"{pin_name} ({pin_package_item[4]})")

    return vid_pin_name_pin_package_dict
