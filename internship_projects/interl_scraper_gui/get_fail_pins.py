import bs4
import re


def find_fail_pins(url, search_fail):
    """
    Find the failed pins in the input failure category
    :param url: the link leading to the .html result page
    :param search_fail: the input failure type
    :return:
    """

    with open(url, 'r') as page:
        soup = bs4.BeautifulSoup(page, 'html.parser')

    # Extract the failure pins
    act_table = soup.find_all('table')[1]

    # Extract all the failure types in this unit
    # Expected output: failure_types = ['Short Failure', 'Open Failure', 'Marginal Type 1',...]
    failure_types = act_table.find_all('tr')[2:]
    # Create the failure list for the unit
    failure_list = [failure.td.getText().strip() for failure in failure_types]

    # Extract all rows
    all_rows = act_table.find_all('tr')

    # Navigate to the desired failure type
    if search_fail in failure_list:
        # Search the failure input position in the failure list
        pos = failure_list.index(search_fail) + 2

        # Extract the failure row
        failure_row = all_rows[pos]

        # Extract the pin names in that fail category
        pins = failure_row.find_all('td')[1]

        # Clean the unnecessary information for the pin name
        pin_list = pins.getText().replace('\n', '').replace(' ', '').strip()

        # Remove the UUT Signals
        signal_regrex = re.compile(r'\(.*?\)')
        pin_list = signal_regrex.sub(r'', pin_list).split(',')

        # Check if the failure pin list is empty or not
        if pin_list:
            return pin_list
        else:
            return ''
    else:
        return ''

if __name__ == '__main__':
    url = 'file:\\\\172.19.249.123\\LabData\\FACR\\VIRAL%20Result\\2024\\CI2405-2936%20RPL%20S8161\\Html_U2L87V3401575_CI2405-2936_1_P_M_20240224_074338\\result.html'
    print(find_fail_pins(url, 'Short Failure'))



