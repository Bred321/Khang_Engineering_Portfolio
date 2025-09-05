from prettytable import PrettyTable


def creating_commonality_table(sort_pin_appearance_dict, pin_package_lists):
    """
    Create and write the commonality table to a file
    :param sort_pin_appearance_dict: keys -> number of appearances, values --> pin list of that appearance value
    :param pin_package_lists: all the pin information including UUT Signal, Package Net List and test result
    :return: the content-filled table
    """
    # Process the data
    appearances = sorted(set(sort_pin_appearance_dict.values()), reverse=True)
    summarized_pin_list = [f"{item[1]} ({item[4]})" for item in pin_package_lists]

    # Create and write the contents to the table
    commonality_table = PrettyTable(["Number of failed units", "Commonality pins"])
    commonality_table._max_width = {"Number of failed units": 20, "Commonality pins": 150}

    appearance_dict = {}
    for appearance in appearances:
        appearance_dict[appearance] = [pin_name for pin_name in list(sort_pin_appearance_dict.keys()) if
                                       sort_pin_appearance_dict[pin_name] == appearance]

    for appearance_value, failed_pins in appearance_dict.items():
        if appearance_value > 1:
            # Prepare a list depicting: unit_VID (package_list_name)
            result_list = [pin_package for pin_package in summarized_pin_list if pin_package.split()[0] in failed_pins]
            # Add the row content to the result
            commonality_table.add_row([appearance_value, ', '.join(result_list)])
            commonality_table.add_row([' --------- ',
                                       '------------------------------------------------------------------- '])

    return commonality_table
