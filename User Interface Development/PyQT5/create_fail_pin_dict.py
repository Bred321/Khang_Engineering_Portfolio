from get_fail_pins import find_fail_pins
import logging


def fail_pin_dict(units_htmls_dictionary, search_fail):
    """
    Create some dictionaries related to later processing
    :param units_htmls_dictionary: "unit_vid" : "link to the .html VIRAL file"
    :param search_fail: the input search failure type (Ex: "Short Failure", "Open Failure", ...)
    :return:
    """
    all_unit_pin_list = []
    vid_fail_pins_dict = {}
    unit_vids = list(units_htmls_dictionary.keys())
    # Loop through each unit VID and open its respective result.html page
    for unit_vid, unit_link in units_htmls_dictionary.items():
        # Find the fail pins in the result.html page based on the search input
        fail_pins = find_fail_pins(unit_link, search_fail)
        # Immediately end the loop if the failure types have no fail pin
        if not fail_pins:
            # TODO: print out the app terminal instead of using "print" statement
            print(f"The unit {unit_vid} no fail pins in this failure type")
            break
        else:
            vid_fail_pins_dict[unit_vid] = fail_pins
            all_unit_pin_list.append(fail_pins)

    return all_unit_pin_list, vid_fail_pins_dict
