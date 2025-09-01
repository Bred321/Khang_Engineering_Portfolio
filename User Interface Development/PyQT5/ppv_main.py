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
from io import StringIO
from analyse_ate_data import analyzing_ate_result
from ppvm_analysis import analyse_ppvm_paths
from ppvs_analysis import analyse_ppvs_paths
from write_to_ppv_excel import writing_to_ppv_excel_file
from webdriver_manager.chrome import ChromeDriverManager
import json



# DRIVER_PATH = r"C:\Users\duongbao\bin\chromedriver.exe"
# Set the chromedriver file location
DRIVER_PATH = r'C:\Users\duongbao\PycharmProjects\Python_Data_Automation\chromedriver.exe'

# Modify the reading and writing permission
# os.chmod(DRIVER_PATH, 0o755)

# Opening the website
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# service = webdriver.ChromeService(executable_path=DRIVER_PATH)
# driver = webdriver.Chrome(service=service, options=options)
# driver.get(web_link)


# Wait before the page exists
def ppv_main_function(case_names, output_directory):
    try:
        for case_name in case_names:
            with open('user_config.json') as f:
                user_configuration_data = json.load(f)

            # # Fetch the PPV test web link
            # web_link = 'https://qscmyfacr.intel.com/AtePpv'
            # # Set the chromedriver file location
            # DRIVER_PATH = user_configuration_data['EDGEDRIVER_PATH']
            # driver = webdriver.Edge()
            # driver.get(web_link)
            web_link = user_configuration_data['FACR_WEB_LINK_ATE_PPV']
            driver = webdriver.Edge()
            driver.get(web_link)
            time.sleep(3)
            driver.refresh()
            global main
            main = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "main-section"))
            )
            # print(main.get_attribute('value'))

            # Search the element
            search_box = main.find_element(By.ID, "caseNumber")
            select_box = Select(main.find_element(By.ID, 'operation'))

            # Select the operation
            select_box.select_by_value('PPV')

            # Input the text
            search_box.send_keys(case_name)
            # Press Entesr
            search_box.send_keys(Keys.RETURN)

            # Browse the table and collect the information
            ate_table = main.find_element(By.TAG_NAME, "table")
            html_ate_table = ate_table.get_attribute('innerHTML')
            # print("Table detected: ", html_ate_table)

            time.sleep(7)

            # Get the table
            dfs = pd.read_html(StringIO(driver.page_source))
            # print('Dataframe: ', dfs)

            # -- DATA EXTRACTION FROM THE WEBSITE --
            # - Extract the data from the ATE table
            # - Extract the whole table data and convert into the Dataframe data type
            ppv_result_table_df = dfs[0]

            # - Delete some non-highly informative columns
            del ppv_result_table_df['FPO']
            del ppv_result_table_df['Temperature']
            del ppv_result_table_df['Temperature.1']
            del ppv_result_table_df['PPVM / CPVMTP']
            del ppv_result_table_df['PPVs / CPVsTP']

            # - Rename some column
            ppv_result_table_df.rename(columns={'Binning': 'PPVM Binning'}, inplace=True)
            ppv_result_table_df.rename(columns={'Result': 'PPVM Result'}, inplace=True)

            ppv_result_table_df.rename(columns={'Binning.1': 'PPVs Binning'}, inplace=True)
            ppv_result_table_df.rename(columns={'Result.1': 'PPVs Result'}, inplace=True)

            ppv_result_table_df.rename(columns={'Comment': 'PPVM Comment'}, inplace=True)
            ppv_result_table_df.rename(columns={'Comment.1': 'PPVs Comment'}, inplace=True)

            ppv_result_table_df.rename(columns={'Datalog': 'PPVM Datalog'}, inplace=True)
            ppv_result_table_df.rename(columns={'Datalog.1': 'PPVs Datalog'}, inplace=True)

            # - Modify the data type
            # print(ppv_result_table_df["PPVs Binning"])
            ppv_result_table_df["PPVs Binning"] = ppv_result_table_df["PPVs Binning"].fillna(0)
            ppv_result_table_df["PPVs Binning"] = ppv_result_table_df["PPVs Binning"].astype('int')
            ppv_result_table_df["PPVs Binning"] = ppv_result_table_df["PPVs Binning"].astype('string')
            # ppv_result_table_df["PPVs Binning"] = ppv_result_table_df["PPVs Binning"].astype('string')

            ppv_result_table_df["PPVM Result"] = ppv_result_table_df["PPVM Result"].apply(lambda x: x[:4])
            ppv_result_table_df["PPVM Result"] = ppv_result_table_df["PPVM Result"].astype('string')

            ppv_result_table_df["PPVs Result"] = ppv_result_table_df["PPVs Result"].apply(lambda x: x[:4])
            ppv_result_table_df["PPVs Result"] = ppv_result_table_df["PPVs Result"].astype('string')
            # Logic
            # Loop through 97 and 99 for PPVS -> if no txt. file was found -> return N/A
            # Look for 95 and .txt files -> Return N/A if no such information was found
            # Fetch the data path
            # Extract the VIDs list

            # ------------------
            data_path = ppv_result_table_df['PPVM Datalog'][0]

            if not data_path:
                empty_bins_series = []
                for unit_vid in list(ppv_result_table_df['VID']):
                    empty_bins_series.append("No bin description found")

                ppv_result_table_df["PPVM Bin Descriptions"] =  pd.Series(empty_bins_series)
            else:
                # Modify the PPV Path
                if len(data_path.split('://')) > 1:
                    modified_ppv_path = '\\\\' + data_path.split('://')[1].replace('/', '\\').replace('%20', ' ')
                elif len(data_path.split('://')) == 1:
                    modified_ppv_path = data_path.replace('/', '\\').replace('%20', ' ')

                # # -- PPVM--
                # Analyse the PPVM data
                ppvm_bins_series = analyse_ppvm_paths(list(ppv_result_table_df['VID']), modified_ppv_path)
               
                # Add the bin description to the output table
                ppv_result_table_df["PPVM Bin Descriptions"] = ppvm_bins_series

            # Format the output table
            ppvm_result_df = pd.concat([ppv_result_table_df["Unit#"],
                                    ppv_result_table_df["VID"],
                                    ppv_result_table_df["PPVM Binning"],
                                    ppv_result_table_df["PPVM Result"],
                                    ppv_result_table_df["PPVM Bin Descriptions"]],
                                    axis=1)

            # -- PPVS--
            # Add comment when the PPV result path is not available
            if not data_path:
                empty_bins_series = []
                for unit_vid in list(ppv_result_table_df['VID']):
                    empty_bins_series.append("No bin description found")

                ppv_result_table_df["PPVs Bin Descriptions"] =  pd.Series(empty_bins_series)
            else:
                ppvs_vid_bins_series = pd.Series(list(ppv_result_table_df['PPVs Binning']), index=list(ppv_result_table_df['VID']))
                ppvs_bins_series = analyse_ppvs_paths(list(ppv_result_table_df['VID']), modified_ppv_path, ppvs_vid_bins_series)
                ppv_result_table_df["PPVs Bin Descriptions"] = ppvs_bins_series

            ppvs_result_df = pd.concat([ppv_result_table_df["Unit#"],
                                        ppv_result_table_df["VID"],
                                        ppv_result_table_df["PPVs Binning"],
                                        ppv_result_table_df["PPVs Result"],
                                        ppv_result_table_df["PPVs Bin Descriptions"]],
                                        axis=1)

            # Export the PPV result to an Excel file
            output_path = os.path.join(output_directory, f'{case_name}_PPV_Result.xlsx')
            ppv_excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
            writing_to_ppv_excel_file(case_name, ppvm_result_df, ppvs_result_df,ppv_excel_writer)
            ppv_excel_writer._save()

            print("The program has finished analyzing the PPV result for the case: ", case_name)
            driver.quit()
    except:
        print("Execution failed, please check your configuration.")
        driver.quit()
        return "Execution failed, please check your configuration."       

    return f"The program has successfully analyze the PPV mode"
