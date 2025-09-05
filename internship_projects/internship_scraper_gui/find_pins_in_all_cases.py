import bs4


def finding_pins_in_all_cases(case_list, units_htmls_dictionary_list, input_pins):
    result_dictionary = {}
    result_dictionary_list = {}
    position = 0
    for case in case_list:
        result_dictionary[case] = {}

    for input_pin in input_pins:
        result_dictionary_list[input_pin] = {}
        for case_dict in units_htmls_dictionary_list:
            for unit_vid, unit_link in case_dict.items():
                with open(unit_link, 'r') as page:
                    soup = bs4.BeautifulSoup(page, 'html.parser')
                    act_table = soup.find_all('table')[-1]
                    all_rows = act_table.find_all('tr')[1:]
                    data = [row.find_all('td') for row in all_rows]
                    all_pins = [pin[1].getText().replace('\xa0', '').strip() for pin in data]
                    if input_pin in all_pins:
                        pos = all_pins.index(input_pin)
                        print(pos)
                        result_dictionary[case_list[position]][unit_vid] = data[pos][-1].getText().replace('\xa0', '').strip()
                    elif input_pin not in all_pins:
                        result_dictionary[case_list[position]][unit_vid] = 'N/A'
            position += 1
            print(result_dictionary)
            print(input_pin)
        result_dictionary_list[input_pin] = result_dictionary
        print(result_dictionary_list)
        position = 0
    print(result_dictionary_list)


if __name__ == '__main__':
    test_list = [{'U1UP912701484': '\\\\172.19.249.123\\LabData\\FACR\\VIRAL Result\\2024\\CI2402-2080 TGP\\Html_U1UP912701484_CI2402-2080_3_F_MS_20240119_025504\\result.html', 'U1V54K0805680': '\\\\172.19.249.123\\LabData\\FACR\\VIRAL Result\\2024\\CI2402-2080 TGP\\Html_U1V54K0805680_CI2402-2080_2_F_MSO_20240119_025339\\result.html', 'U1WW478101830': '\\\\172.19.249.123\\LabData\\FACR\\VIRAL Result\\2024\\CI2402-2080 TGP\\Html_U1WW478101830_CI2402-2080_1_F_MSO_20240119_025243\\result.html'}, {'M3R66T8100470': '\\\\172.19.249.123\\LabData\\FACR\\VIRAL Result\\2024\\CI2417-6379 RPL S8161\\Html_M3R66T8100470_CI2417-6379_1_F_MSO_20240607_015629\\result.html'}]
    cases = ['CI2402-2080', 'CI2417-6379']
    finding_pins_in_all_cases(cases, test_list, ['J3', 'J5'])