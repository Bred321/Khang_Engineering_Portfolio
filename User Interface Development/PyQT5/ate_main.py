from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging
import os
import time
import pandas as pd
import json
from io import StringIO
from analyse_ate_data import analyzing_ate_result
from navigate_ate_result_path import navigating_to_ate_result_path
from write_to_ate_excel import writing_to_ate_excel_file
from ate_class_hot_df_processing import processing_ate_class_hot_df_processing
from ate_class_cold_df_processing import processing_ate_class_cold_df_processing
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def ate_main_function(case_names, output_directory):
    try:
        for case_name in case_names:
            # -- Initiate the browser
            # Process the user configuration data
            print("Processing the case: ", case_name)
            with open('user_config.json') as f:
                user_configuration_data = json.load(f)
            # Set the chromedriver file location
            # # Modify the reading and writing permission
            # os.chmod(DRIVER_PATH, 0o755)

            # Opening the website
            # options = webdriver.ChromeOptions()
            # options.add_experimental_option("detach", True)
            web_link = user_configuration_data['FACR_WEB_LINK_ATE_PPV']
            # service = webdriver.ChromeService(executable_path=DRIVER_PATH)
            # driver = webdriver.Chrome(service=service, options=options)
            driver = webdriver.Edge()
            driver.get(web_link)

            # -- Wait before the page exists
        
            # --  INITIATE AND OPEN THE WEBSITE
            time.sleep(3)  
            driver.refresh()
            global main 
            main = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "main-section"))
            )

            # Search the element
            search_box = main.find_element(By.ID, "caseNumber")
            select_box = Select(main.find_element(By.ID, 'operation'))

            # Select the operation
            select_box.select_by_value('ATE - Class Hot')

            # Input the text
            search_box.send_keys(case_name)

            # Press Enter
            search_box.send_keys(Keys.RETURN)

            # Browse the table and collect the information
            ate_table = main.find_element(By.TAG_NAME, "table")
            html_ate_table = ate_table.get_attribute('innerHTML')

            # - Wait for the data to fully load
            time.sleep(7)

            # - Get the ATE Result Table
            dfs = pd.read_html(StringIO(driver.page_source))

            # -- DATA EXTRACTION FROM THE WEBSITE --
            # - Extract the data from the ATE table
            # - Extract the whole table data and convert into the Dataframe data type
            ate_result_table_df = dfs[0]
            output_path = os.path.join(output_directory, f'{case_name}_ATE_Result.xlsx')
            ate_excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

            # -- PROCESSING THE DATA
            current_hot_tp_df, original_hot_tp_df = processing_ate_class_hot_df_processing(ate_result_table_df)

            # -- WRITING THE ATE HOT DATA RESULT TO AN EXCEL FILE
            writing_to_ate_excel_file(case_name, current_hot_tp_df, original_hot_tp_df, 'ATE - Class Hot', ate_excel_writer)

            # - Processing the ATE - CLASS COLD data
            select_box.select_by_value('ATE - Class Cold')
            ate_table = main.find_element(By.TAG_NAME, "table")
            html_ate_table = ate_table.get_attribute('innerHTML')
            time.sleep(7)
            dfs_cold = pd.read_html(StringIO(driver.page_source))
            ate_result_table_df_cold = dfs_cold[0]
            current_cold_tp_df, original_cold_tp_df = processing_ate_class_cold_df_processing(ate_result_table_df_cold)
            
            # -- WRITING THE ATE COLD DATA RESULT TO AN EXCEL FILE
            writing_to_ate_excel_file(case_name, current_cold_tp_df, original_cold_tp_df, 'ATE - Class Cold', ate_excel_writer)
            
            # Save the contents to an Excel file
            ate_excel_writer._save()
            driver.quit()

            # -- LOGGING THE SUCCESS MESSAGE
            print(f"The program has successfully analyze the case {case_name}")
            # - Exit the browser application

    except:
        print("Execution failed, please check your configuration.")
        driver.quit()
        return "Execution failed, please check your configuration."

    return f"The program has successfully analyze the ATE mode"

# Functional verification testing
# if __name__ == "__main__":
#     ate_main_function(["CI2430-0677"], "C:/Users/duongbao/Downloads")


