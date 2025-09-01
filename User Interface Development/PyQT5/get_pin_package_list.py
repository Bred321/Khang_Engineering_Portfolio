import bs4


def get_pin_functional_package_list(url):
    """
    Get the list of all the pins in a unit
    :param url: a link leading to the result.html
    :return: a list of all the pins in a unit
    """
    print('The processing link is: ', url)
    with open(url, 'r') as page:
        soup = bs4.BeautifulSoup(page, 'html.parser')

    # Extract the failure pins
    act_table = soup.find_all('table')[-1]

    pin_package_names = act_table.find_all('tr')[1:]
    pin_package_name_list = [item.getText().split('\n\xa0')[1:] for item in pin_package_names]

    return pin_package_name_list
