from collections import Counter


def finding_commonality(vid_fail_pins_dict):
    # Create a set containing all the failure pins of all units
    all_failure_pins = set(pin for pins in vid_fail_pins_dict.values() for pin in pins)

    # Count the appearance number of each pin and record the vids they appear in
    pin_appearance_counter = Counter()
    pin_vid = {pin: [] for pin in all_failure_pins}

    for vid, fail_pins in vid_fail_pins_dict.items():
        for pin in fail_pins:
            pin_vid[pin].append(vid)
            pin_appearance_counter[pin] += 1

    # Sort the pins by their frequency of appearance
    sort_pin_appearance_dict = dict(pin_appearance_counter.most_common())

    # Create a dictionary with the appearing frequency in more than one unit
    chosen_list = {pin: vids for pin, vids in pin_vid.items() if pin_appearance_counter[pin] > 1}
    sorted_chosen_list = dict(sorted(chosen_list.items(), key=lambda item: len(item[1]), reverse=True))

    return sorted_chosen_list, sort_pin_appearance_dict
