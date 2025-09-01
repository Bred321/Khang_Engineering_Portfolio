import logging
import os
import playwright.sync_api
from playwright.sync_api import sync_playwright


# def run(p, url, unit_vid, image_folder, pin):
#     """
#     p: library-specialized object
#     url: link to the IV Curve
#     unit_vid: Unit VID
#     image_folder: image storage location
#     pin: the input pin to capture the IV Curve
#     return: None
#     """
#     # Launch the browser
#     browser = p.chromium.launch(channel="chrome")
#     # Opens a new browser page
#     page = browser.new_page()
#     # navigate to the website
#     page.goto(url)
#     image_file = image_folder + f"\\{unit_vid}_{pin}.png"
#     # Take a full page screenshot of the IV curve
#     page.screenshot(path=image_file, full_page=True)
#     # Close the browser
#     browser.close()

    # take a full-page screenshot
    # always close the browser
def run(url, unit_vid, image_folder, pin):
    """
    p: library-specialized object
    url: link to the IV Curve
    unit_vid: Unit VID
    image_folder: image storage location
    pin: the input pin to capture the IV Curve
    return: None
    """
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(channel="chrome")
        # Opens a new browser page
        page = browser.new_page()
        # navigate to the website
        page.goto(url)
        image_file = image_folder + f"\\{unit_vid}_{pin}.png"
        # Take a full page screenshot of the IV curve
        page.screenshot(path=image_file, full_page=True)
        # Close the browser
        browser.close()


