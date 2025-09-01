import os
import logging


def create_image_link(url, pin_name):
    """
    Create the link leading to the image of the IV Curve to take the screenshot
    :param url: the result.html VIRAL result of the unit
    :param pin_name: the pin that needs the image of an IV Curve
    :return: the complete feasible link to the unit's image
    """
    # print("Processing link: ", url)
    split_link = url.split(' ')
    inter_link = '%20'.join(split_link)
    complete_link = 'file:' + inter_link[:-12] + f"\\Data\\IV.html?pid={pin_name}"
    print("Continue processing link: ", complete_link)
    # Return the complete link
    return complete_link
