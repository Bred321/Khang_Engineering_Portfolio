import pandas as pd
import re
import logging
import os


def clean_excel_sheet(df):
    """Remove addtional Excel sheet info the bring table's names to the top

    Args:
        df (_DataFrame_): the input Dataframe

    Returns:
        _DataFrame_: the Dataframe after processing
    """
    # Only process the row after the one containing the "Asset ID" word. Any row above that
    # will be deleted
    first_asset_id_idx = df.iloc[:, 0].eq("Asset ID").idxmax()
    df.columns = df.iloc[first_asset_id_idx]
    df = df.iloc[first_asset_id_idx+1:].reset_index(drop=True)
    return df


def clean_relationship_sheet(df):
    """Delete the addtional information on top of the table

    Args:
        df (_DataFrame_): the input Dataframe

    Returns:
        _DataFrame_: the Dataframe after processing
    """
    # Only process the row after the one containing the "Asset ID" word. Any row above that
    # will be deleted
    first_asset_id_idx = df.iloc[:, 0].eq("Parent Asset").idxmax()
    df.columns = df.iloc[first_asset_id_idx]
    df = df.iloc[first_asset_id_idx+1:].reset_index(drop=True)
    return df


def sort_columns(column_name, sheet_name):
    """Sort the column names in the correct alphabetical and numerial order"""
    well_regEx = re.compile(r'production', re.IGNORECASE)
    manifold_regEx = re.compile(r'manifold', re.IGNORECASE)
    gas_lift_regEx = re.compile(r'gas', re.IGNORECASE)
    water_injection_regEx = re.compile(r'water', re.IGNORECASE)
    gx_px_regEx = re.compile(r'(?:GX|PX)-?(\d+)', re.IGNORECASE)
    gm_pm_regEx = re.compile(r'(?:GM|PM|PPI|PPT)-?(\d+)\s*(?:H|SCM: ICM)?(\d+)', re.IGNORECASE)
    wx_regEx = re.compile(r'WX-(\d+)', re.IGNORECASE)
    ppi_regEx = re.compile(r'ppi', re.IGNORECASE)

    # Production well columns sorting logic
    if well_regEx.search(sheet_name) and gx_px_regEx.search(column_name):
        match = gx_px_regEx.search(column_name)
        if match:
            return int(match.group(1))
        return float('inf')
    # Production manifold columns sorting logic
    elif manifold_regEx.search(sheet_name) and gm_pm_regEx.search(column_name):
        match = gm_pm_regEx.search(column_name)
        if ppi_regEx.search(column_name):
            return float('inf')
        if (match.group(1)) and (match.group(2)):
            return int(match.group(1)) * 10 + int(match.group(2))
        elif (not match.group(2)) and (match.group(1)) :
            return int(match.group(1))
        else:
            return float('inf')
    # Gas Lift columns sorting logic
    elif gas_lift_regEx.search(sheet_name) and gx_px_regEx.search(column_name):
        match = gx_px_regEx.search(column_name)
        if match:
            return int(match.group(1))
        return float('inf')
    elif water_injection_regEx.search(sheet_name) and wx_regEx.search(column_name):
        match = wx_regEx.search(column_name)
        if match:
            return int(match.group(1))
        return float('inf')
    # For other cateogories, combine all the sorting logic to product the best possible results
    else:
        match = gx_px_regEx.search(column_name)\
                or gm_pm_regEx.search(column_name)\
                or wx_regEx.search(column_name)
        if match:
            return int(match.group(1))
        return float('inf')


def extract_sheet_names(df_asset_list, df_device, asset_types):
    """Generate the sheet names

    Args:
        df_asset_list (_DataFrame_): the asset list in the field Excel file
        df_device (_DataFrame_): the device (Ex: VFM, Choke,.. ) sheet in the configuration fiels
        asset_types (_DataFrame_): _description_

    Returns:
        _list_: a list of sheet names
    """
    result_assets = []
    asset_type_list = list(df_asset_list["Asset Type"])
    asset_type_whole_string = "".join(asset_type_list)
    for asset_type in asset_types:
        asset_type_original = df_device[df_device["columnTitle"] == asset_type]["assetType"]
        asset_type_original = list(asset_type_original)[0]
        asset_regEx = re.compile(asset_type_original)
        if asset_regEx.search(asset_type_whole_string):
            result_assets.append(asset_type)
        else:
            continue
    return result_assets


def extract_row_title(excel_asset_relationship_file_path, device, df_ims_tag_output, 
                      df_asset_list, df_relationship_list, 
                      df_device, tag_name, path, 
                      row_title, sheet_name, col_list):
    """Generate the row's contents

    Args:
        excel_asset_relationship_file_path (_str_): the path pointing to the asset Excel file
        device (_str_): the device name (Ex: VFM, Choke,..)
        df_ims_tag_output (_Dataframe_): the IMSTagOutput sheet in the field Excel file
        df_asset_list (_Dataframe_): the asset list in the field Excel file
        df_relationship_list (_Dataframe_): the Relationship sheet in the field Excel file
        df_device (_Dataframe_): the Dataframe of that device in the configuration file
        tag_name (_str_): the tag name fetched from the "assetType" column of the device in the config Excel file
        path (_str_): the tag name fetched from the "path" column of the device in the config Excel file
        row_title (_str_): the tag name fetched from the "rowTitle" column of the device in the config Excel file
        sheet_name (_str_): the currently processed sheet name
        col_list (_str_): the column names list of the currently processed sheet

    Returns:
        _list_: the output row contents stored in a list
    """
    # Regular expressions
    tag_regEx = re.compile(re.escape(tag_name))
    other_device_regEx = re.compile(r'electrical|comms|sensors|controls equipment', re.IGNORECASE)
    well_regEx = re.compile(r'production', re.IGNORECASE)
    manifold_regEx = re.compile(r'manifold', re.IGNORECASE)
    gas_lift_regEx = re.compile(r'gas', re.IGNORECASE)
    water_injection_regEx = re.compile(r'water', re.IGNORECASE)
    status_regEx = re.compile(r'status', re.IGNORECASE)
    hpu_regEx = re.compile(r'hpu', re.IGNORECASE)
    gx_px_regEx = re.compile(r'(?:GX|PX)-?(\d+)', re.IGNORECASE)
    gm_pm_regEx = re.compile(r'(?:GM|PM|PPI|PPT)-?(\d+)', re.IGNORECASE)
    wx_regEx = re.compile(r'WX-\d+', re.IGNORECASE)
    h1_f1_regEx = re.compile(r'H1|F1', re.IGNORECASE)
    h2_f2_regEx = re.compile(r'H2|F2', re.IGNORECASE)
    ppi_regEx = re.compile(r'ppi_', re.IGNORECASE)
    ppt_regEx = re.compile(r'ppt_', re.IGNORECASE)
    m_field_regEx = re.compile(r'M-Field', re.IGNORECASE)
    p_field_regEx = re.compile(r'P-Field', re.IGNORECASE)

    # Pre-defined variables
    tag_type_list = list(df_ims_tag_output["Tag Type"])
    tag_type_whole_string = " ".join(tag_type_list)
    row_list_returned = []
    final_rows_list_returned = []
    path_searched = path.split("/")[-1]
    match_suffix = re.search(r'"([^""]*)"', row_title)
    result_suffix = match_suffix.group(1).strip()
    asset_ids_in_asset_list_sheet = []

    # Check if the tag name in the device sheet can be found in the Tag Type in the IMSTagOutput sheet
    if not tag_regEx.search(tag_type_whole_string):
        return []
    
    if other_device_regEx.search(device):
        for item in list(df_asset_list[df_asset_list["Asset Type"] == path_searched]["Asset ID"]):
            asset_ids_in_asset_list_sheet.append(item)
    else:
        # Extract the asset id for that row
        for item in list(df_asset_list[df_asset_list["Asset Type"] == path_searched]["Asset ID"]):
            if well_regEx.search(sheet_name) and gx_px_regEx.search(item):
                asset_ids_in_asset_list_sheet.append(item)
            elif manifold_regEx.search(sheet_name) and gm_pm_regEx.search(item):
                asset_ids_in_asset_list_sheet.append(item)
            elif gas_lift_regEx.search(sheet_name) and gx_px_regEx.search(item):
                asset_ids_in_asset_list_sheet.append(item)
            elif water_injection_regEx.search(sheet_name) and wx_regEx.search(item):
                asset_ids_in_asset_list_sheet.append(item)
            elif status_regEx.search(sheet_name) or hpu_regEx.search(sheet_name):
                asset_ids_in_asset_list_sheet.append(item)

    # -- ROW EXTRACTION --
    # Example case 1:["Cv Measured (Bara)"]
    if len(row_title.split(",")) < 2:
        row_list_returned.append([result_suffix])
    # Example case 2: [*/VFM - Element Grouping - Production Well/VFM - PT Node{{name}}, " Pressure (Bara)"]
    else:
        for asset_id in asset_ids_in_asset_list_sheet:
            lowest_level_asset_name = list(df_asset_list[df_asset_list["Asset ID"] == asset_id]["Lowest Level Asset Name"])[0]
            row_name = lowest_level_asset_name + ' ' + result_suffix
            if [row_name] not in row_list_returned:
                row_list_returned.append([row_name])

    # -- TAG EXTRACTION -- 
    # Example of row_list_returned [['Cv Measured (Bara)']]
    # Example of asset_ids_in_asset_list_sheet: ['U_VFM- U1A (GX-05) PCV', 'U_VFM- U1B (GX-06) PCV']
    # Example of row_list_returned with tags: [['Cv Measured (Bara)', 'ONGC_HMI_U_FIELD.U_FIELD.U1A_SHIFT.VFM.PCV.CvMeasured', 'ONGC_HMI_U_FIELD.U_FIELD.U1B.VFM.PCV.CvMeasured']]
    if len(path.split("/")) < 3:
        for row_list in row_list_returned:
            for asset_id in asset_ids_in_asset_list_sheet:
                tag_id_one_ele_list = list(df_ims_tag_output[(df_ims_tag_output["Asset ID"] == asset_id) & (df_ims_tag_output["Tag Type"] == tag_name)]["Tag ID"])
                tag_id = tag_id_one_ele_list[0] if tag_id_one_ele_list else ' '
                row_list.append(tag_id)
        return row_list_returned
    
    for row_list in row_list_returned:
        for asset_id in asset_ids_in_asset_list_sheet:
            # If the sheet name is status, fetch the tag id directly from the tag type, otherwise
            # perform other calculations
            if status_regEx.search(sheet_name):
                tag_id = list(df_ims_tag_output[(df_ims_tag_output["Tag Type"] == tag_name)]["Tag ID"])[0]
                row_list.append(tag_id)
            else:
                lowest_level_asset_name = list(df_asset_list[df_asset_list["Asset ID"] == asset_id]["Lowest Level Asset Name"])[0]
                asset_name_regEx = re.compile(re.escape(lowest_level_asset_name), re.IGNORECASE)
                # Example: Lowest level name : VFM DHPT, and row_list[0]: VFM DHPT Pressure (Bara)
                row_name = row_list[0]
                if asset_name_regEx.search(row_name):
                    tag_id_one_ele_list = list(df_ims_tag_output[(df_ims_tag_output["Asset ID"] == asset_id) & (df_ims_tag_output["Tag Type"] == tag_name)]["Tag ID"])
                    tag_id = tag_id_one_ele_list[0] if tag_id_one_ele_list else ' '
                    row_list.append(tag_id)
                    if h1_f1_regEx.search(row_name):
                        row_list.append(' ')
                    elif h2_f2_regEx.search(row_name):
                        row_list.insert(1, ' ')
                    if ppt_regEx.search(tag_id) and m_field_regEx.search(excel_asset_relationship_file_path):
                        row_list.insert(1, tag_id)
                        row_list.insert(1, ' ')
                        row_list.insert(1, ' ')
                        del row_list[-1]
                    if ppi_regEx.search(tag_id) and p_field_regEx.search(excel_asset_relationship_file_path):   
                        for i in range(len(col_list) - len(row_list)):
                            row_list.insert(1, ' ')       

    # Special treatment for P-Field manifold headers -> Aligning the tag id with manifold name and flowline
    if p_field_regEx.search(excel_asset_relationship_file_path) and manifold_regEx.search('Manifold'):   
        for row_list in row_list_returned:
            if h2_f2_regEx.search(row_list[0]):
                row_list[2], row_list[3] = row_list[3], row_list[2]   

    # Return the list of ['row name', 'tag_id_1', 'tag_id_2', ....]
    for item in row_list_returned:
        print(f"Comparing {len(item)} with {len(col_list)}")
        if len(item) < len(col_list):
            item += ' ' * (len(col_list) - len(item)) 
        if len(item) > len(col_list):
            item = ' ' * len(col_list)
    # Return all the rows within a sheet
    return row_list_returned
    

def extract_col_title(input_str):
    """Find the column title from the columnTitle column in the configuration file

    Args:
        input_str (_str): ["Acoustic Raw - OutputA (Counts)"] for example

    Returns:
        _str_: the string within the double quotes, Acoustic Raw - OutputA (Counts) for example
    """
    match = re.search(r'/([^{}]*){', input_str)
    if match:
        result = match.group(1).strip()
        return result
    return input_str


def generate_excel_files(device, 
                        excel_config_file_path, 
                        excel_asset_relationship_file_path,
                        output_folder_path):
    """Generate the output information to write to the Excel file

    Args:
        device (_str_): device name
        excel_config_file_path (_str_): Excel configuration file path 
        excel_asset_relationship_file_path (_str_): Execel asset relationship file path
    """
    # Read Excel files and sheets
    df_config = pd.read_excel(excel_config_file_path, sheet_name=None)
    df_search = pd.read_excel(excel_asset_relationship_file_path, sheet_name=None)
    df_device = df_config[device]
    df_relationship_list = df_search['Relationship list']
    df_asset_list = df_search['Asset list']
    df_ims_tag_output = df_search['IMSTagOutput']
    other_device_regEx = re.compile(r'electrical|comms|sensors|controls equipment', re.IGNORECASE)

    # Clean and format the input Excel files
    df_asset_list = clean_excel_sheet(df_asset_list)
    df_ims_tag_output = clean_excel_sheet(df_ims_tag_output)
    df_relationship_list = clean_relationship_sheet(df_relationship_list)

    # Create a list of sheet names
    asset_types_sheet = list(df_device[df_device['componentName'] == 'AssetType']['columnTitle'])
    asset_types_original = []
    asset_types_sheet_filtered = extract_sheet_names(df_asset_list, df_device, asset_types_sheet)
    for asset_type in asset_types_sheet_filtered:
        asset_types_original.append(list(df_device[df_device['columnTitle'] == asset_type]['assetType'])[0])

    # Create a DataFrame for each sheet name
    df_sheet_df_dict = {}
    for asset_type in asset_types_sheet_filtered:
        df_sheet_df_dict[asset_type] = pd.DataFrame()
   
    # Generate columns names for each sheet
    dict_sheet_name_to_cols = {} # contains 'sheet_name' : list(column_names)
    for asset_type_original in asset_types_original:
        sheet_name = list(df_device[(df_device["assetType"] == asset_type_original) & (df_device["rowTitle"].isna())]["columnTitle"])[0]
        columns = set(df_asset_list[df_asset_list["Asset Type"] == asset_type_original]["Short Name"])
        columns = sorted(list(columns), key=lambda x: sort_columns(x, sheet_name))
        columns.insert(0, "Tags")
        dict_sheet_name_to_cols[sheet_name] =  columns

    # Generate all rows for each sheet
    dict_sheet_name_to_rows = {} # contains 'sheet_name' : pd.Dataframe(rows)
    for asset_type_original in asset_types_original:
        result_list = []
        sheet_name = list(df_device[(df_device["assetType"] == asset_type_original) & (df_device["rowTitle"].isna())]["columnTitle"])[0]
        row_titles_list = list(df_device[(df_device["assetType"] == asset_type_original) & (df_device["componentName"] == "OverviewTable")]["rowTitle"].dropna())
        path_list = list(df_device[(df_device["assetType"] == asset_type_original) & (df_device["componentName"] == "OverviewTable")]["path"].dropna())
        tag_name_list = list(df_device[(df_device["assetType"] == asset_type_original) & (df_device["componentName"] == "OverviewTable")]["tagName"].dropna())
        end_index = len(row_titles_list)
        for index in range(end_index):
            returned_rows_list = extract_row_title(excel_asset_relationship_file_path, device, df_ims_tag_output, df_asset_list, 
                                                   df_relationship_list, df_device, tag_name_list[index], 
                                                   path_list[index], row_titles_list[index], sheet_name,
                                                   list(dict_sheet_name_to_cols[sheet_name]))
            for item_list in returned_rows_list:
                result_list.append(item_list)
            df_result = pd.DataFrame(result_list, columns=dict_sheet_name_to_cols[sheet_name])
        dict_sheet_name_to_rows[sheet_name] =  df_result


    # Populate each data frame with columns
    df_sheet_df_dict = {} # contains 'sheet_name' : 'contents'
    for sheet_name, column_names in dict_sheet_name_to_cols.items():
        df_sheet_df_dict[sheet_name] = pd.DataFrame(columns=column_names)
        df_sheet_df_dict[sheet_name] = pd.concat([df_sheet_df_dict[sheet_name], dict_sheet_name_to_rows[sheet_name]], ignore_index=True)

    # Specify the output path
    file_name = f"{device}-{excel_asset_relationship_file_path.split("\\")[-1]}"
    file_path = file_name + '' + ".xlsx"
    save_path = os.path.join(output_folder_path, file_path)
    # Write the content to the output file
    with pd.ExcelWriter(save_path) as writer:
        for sheet_name, df_name in df_sheet_df_dict.items():
            df_name.to_excel(writer, sheet_name=sheet_name, index=False)


def main():
    """Main function - Contain user inputs and main execution function
    """
    #! -- User input --
    #! Please use "\\" for Windows path
    excel_config_file_path = 'config\\ONGC 98-2 View Config D38.xlsx'
    excel_asset_relationship_file_path = 'config\\AAA432538 Annex A A-Field Config Tag_Asset_Rel - Rev 002 D20 1.xlsx'
    output_folder_path = 'output_test'
    # Full devices items 
    device_list = ['Electrical', 'Comms', 'Choke', 'VFM', 'Hydraulic', 'Sensors', 'Controls Equipment', 'Actuator']
    # Device list for isolating a device
    device_list_test = ['Controls Equipment']

    #! -- Main Function Execution --
    # Create an output directory if it has not been created
    try:
        print('----- LOGGING -----')
        if os.path.isdir(output_folder_path):
            print(f'SAVING: The output folder is ready at the location: "{os.path.abspath(output_folder_path)}"')
            pass
        else:
            os.mkdir(output_folder_path)
            print(f'SAVING: A folder is created at the location: "{os.path.abspath(output_folder_path)}"')
    except Exception as e:
        print('\n-- ERROR --')
        logging.error("An error occurred: {e}\n", exc_info=True)
        print("\n DEBUG: Please check the input and try again")
        
    # Loop through each device in the list
    successful_devices = []
    failed_devices = []
    error_logs = {}
    for device in device_list_test:
        try:
            generate_excel_files(device, 
                            excel_config_file_path=excel_config_file_path, 
                            excel_asset_relationship_file_path=excel_asset_relationship_file_path,
                            output_folder_path=output_folder_path)
            successful_devices.append(device)
            print(f'PROCESS: "{device}" Successful')
            continue
        except Exception as e:
            failed_devices.append(device)
            error_logs[device] = e
            print(f'PROCESS: "{device}" Failed')
            continue

    # Report the program results
    print('\n----- RESULT REPORT -----')
    print(f"Successful device(s): {", ".join(successful_devices)}")
    print(f"Failed device(s): {", ".join(failed_devices)}\n")
    # Report the errors if any
    print('----- ERROR LOGS -----')
    for item, error in error_logs.items():
        print(f'Device: {item} | Errror: "{error}"')


if __name__ == '__main__':
    #! ----- Current Script Performacne -----
    #! U-Field: Passed 100%
    #! R-Field: Failed Control Equipment (document related). 
    #! A-Field: Failed Control Equipment (document related).
    #! P-Field: Passed 100%
    #! M-Field: Passed 100%
    #! Sensors device (for all fields): containing both GX and GM or WX
    #! Please check the columns in the output files to validate their correctness
    main()


