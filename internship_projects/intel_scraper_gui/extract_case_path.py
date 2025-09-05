import os


# Having the product makes the function finishes much faster (0.00004 versus 0.02)
def not_having_product_name(case_name_input, year_input):
    PATH = "\\\\172.19.249.123\\LabData\\FACR\\VIRAL Result"
    # PATH = "//172.19.249.123/LabData/FACR/VIRAL Result"
    # year_path = os.path.join(PATH, year_input)
    year_path = PATH + f"\\{year_input}"
    files = os.listdir(year_path)

    for file in files:
        if case_name_input in file:
            case_path = year_path + f"\\{file}"
            # case_path = os.path.join(year_path, file)
            return os.path.normpath(case_path)

    return None


def having_product_name(case_name_input, year_input):
    """
    Construct the input case folder in the shared VIRAL folder
    :param case_name_input: the input case name from the user
    :param year_input: the input year from the user
    :return: a string representing the case path
    """
    # The default base bath leading to the shared VIRAL folder
    PATH = "\\\\172.19.249.123\\LabData\\FACR\\VIRAL Result"
    # PATH = "//172.19.249.123/LabData/FACR/VIRAL Result"

    # Construct a link to the folder of that case
    year_path = os.path.join(PATH, year_input)
    case_path = os.path.join(year_path, case_name_input)

    return os.path.normpath(case_path)


def get_case_path(case_name_input, year_input):
    """
    Construct the input case foler in the shared VIRAL folder
    :param case_name_input: the input case name from the user
    :param year_input: the input year from the user
    :return: a string representing the case path
    """
    # The default base bath leading to the shared VIRAL folder
    getting_the_path = not_having_product_name if len(case_name_input.split()) == 1 else having_product_name

    return getting_the_path(case_name_input, year_input)
