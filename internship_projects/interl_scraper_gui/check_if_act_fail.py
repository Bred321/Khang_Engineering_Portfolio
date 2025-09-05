import bs4


def checking_if_act_fail(url):
    with open(url, 'r') as page:
        soup = bs4.BeautifulSoup(page, 'html.parser')

    # Extract the failure pins
    act_table = soup.find_all('table')[1]

    # Extract all the failure types in this unit
    # Expected output: failure_types = ['Short Failure', 'Open Failure', 'Marginal Type 1',...]
    failure_types = act_table.find_all('tr')[2:]
    # Create the failure list for the unit
    failure_list = [failure.td.getText().strip() for failure in failure_types]

    test_conditions = ['Short Failure', 'Open Failure']
    result = []

    failure_positions = {
        'Short Failure': 2,
        'Open Failure': 3
    }

    # Extract all rows
    all_rows = act_table.find_all('tr')

    # Navigate to the desired failure type
    for fail in test_conditions:
        if fail in failure_list:
            # Search the failure input position in the failure list
            pos = failure_positions[fail]

            # Extract the failure row
            failure_row = all_rows[pos]

            # Extract the pin names in that fail category
            pins = failure_row.find_all('td')[1]

            # Clean the unnecessary information for the pin name
            pin_list = pins.getText().replace('\n', '').replace(' ', '').strip()

            # Confirm whether the unit failed ACT or not
            # 'True' stands for ACT failure
            result.append('True' if pin_list == '-' else 'False')

    # Return True if the unit failed ACT
    return all(res == 'True' for res in result)
