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
import numpy as np
from io import StringIO
from analyse_ate_data import analyzing_ate_result
from navigate_ate_result_path import navigating_to_ate_result_path
from write_to_ate_excel import writing_to_ate_excel_file


def processing_ate_class_hot_df_processing(ate_result_table_df):
    # - Empty table verification
    nan_verification = np.isnan(ate_result_table_df['Binning'])
    if all(nan_verification):
        current_df = pd.DataFrame({
                'Unit#' : ['N/A'],
                'VID' : ['N/A'],
                'Current Class Cold TP Binning': ['N/A'],
                'Current Class Cold TP Result' : ['N/A'],
                'Current TP Bin Description' : ['N/A']
                })
        original_df = pd.DataFrame({
                'Unit#' : ['N/A'],
                'VID' : ['N/A'],
                'Original Class Cold TP Binning': ['N/A'],
                'Original Class Cold TP Result' : ['N/A'],
                'Original TP Bin Description' : ['N/A']
                })
        return (current_df, original_df)
    else:
        # - Rename some columns
        ate_result_table_df.rename(columns = {'Binning':'Current Class Hot TP Binning'}, inplace = True)
        ate_result_table_df.rename(columns = {'Binning.1':'Original Class Hot TP Binning'}, inplace = True)
        ate_result_table_df.rename(columns = {'Result':'Current Class Hot TP Result'}, inplace = True)
        ate_result_table_df.rename(columns = {'Result.1':'Original Class Hot TP Result'}, inplace = True)

        # - Extract the unit VID
        unit_number = ate_result_table_df['Unit#'].astype('string')
        unit_vids = ate_result_table_df['VID'].astype('string')

        # - Extract the binning for the current and orginal TP
        current_hot_binning = ate_result_table_df['Current Class Hot TP Binning']
        original_hot_binning = ate_result_table_df['Original Class Hot TP Binning']

        # - Extract the result for the current and orginal TP
        current_hot_tp_result = ate_result_table_df['Current Class Hot TP Result']
        original_hot_tp_result = ate_result_table_df['Original Class Hot TP Result']

        # - Fill out NULL values
        current_hot_binning = current_hot_binning.fillna(0)
        original_hot_binning = original_hot_binning.fillna(0)

        # - Change the binning data type from float to string
        current_hot_binning = current_hot_binning.astype('int')
        original_hot_binning = original_hot_binning.astype('int')
        current_hot_binning = current_hot_binning.astype('string')
        original_hot_binning = original_hot_binning.astype('string')

        # - Extract the TP name
        for tp_item in ate_result_table_df['CurrentTP']:
            if tp_item:
                tp_name = tp_item

        # - Modify the result text (omitting the triangle sign)
        current_hot_tp_result = current_hot_tp_result.apply(lambda x: x[:4])
        current_hot_tp_result = current_hot_tp_result.astype('string')
        original_hot_tp_result = original_hot_tp_result.apply(lambda x: x[:4])
        original_hot_tp_result = original_hot_tp_result.astype('string')

        # -- ANALYZE THE DATA -- 
        # - Analyze current TP binning
        # if all(ate_result_table_df[])
        current_hot_binning_description = analyzing_ate_result(current_hot_binning, current_hot_tp_result, tp_name)
        ate_result_table_df['Current TP Bin Description'] = current_hot_binning_description

        # - Analyze original TP binning
        original_hot_binning_description = analyzing_ate_result(original_hot_binning, original_hot_tp_result, tp_name)
        ate_result_table_df['Original TP Bin Description'] = original_hot_binning_description

        # print(ate_result_table_df['Current TP Bin Description'])

        # Export the result to an Excel file
        current_tp_df = pd.concat([unit_number, unit_vids, current_hot_binning, current_hot_tp_result, ate_result_table_df['Current TP Bin Description']], axis=1)
        original_tp_df = pd.concat([unit_number, unit_vids, original_hot_binning, original_hot_tp_result, ate_result_table_df['Original TP Bin Description']], axis=1)

        return current_tp_df, original_tp_df