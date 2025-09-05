def check_blank(input_text):
    if input_text:
        return input_text
    else:
        return


def getting_case_pins_dict(case_list, pin_lists):
    """
    Create a dictionary of case name with its responding failed pins
    :param case_list: the list of input cases
    :param pin_lists: the input pin list for each case
    :return: a dictionary
    """
    pin_dict = {}
    name_pos = 0
    insert_text = ""

    # Creating a dictionary
    for pos in range(len(pin_lists)):
        if pin_lists[pos] == '[':
            pin_dict[case_list[name_pos]] = []
        elif pin_lists[pos].isalnum():
            insert_text += pin_lists[pos]
        elif pin_lists[pos] == "," and pin_lists[pos - 1] != ']':
            pin_dict[case_list[name_pos]].append(insert_text)
            insert_text = ""
        elif pin_lists[pos] == ']':
            pin_dict[case_list[name_pos]].append(check_blank(insert_text))
            insert_text = ""
            name_pos += 1

    return pin_dict
