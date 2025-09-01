import os
import json


def navigating_to_bindef_file(tpl_path):
    # Find the Bindef file in the directory
    for file in os.listdir(tpl_path):
        if 'bindefinition' in file.lower():
            return os.path.join(tpl_path, file)


def navigating_to_ate_result_path(test_program_name):
    # Open the json file
    with open('user_config.json') as f:
        user_configuration_data = json.load(f)

    # Get the product ATE path
    # Match the product name based on the TP and construct the equivalent path
    for product_name in user_configuration_data["ATE_RESULT_PATH"].keys():
        if product_name in test_program_name.upper():
            product_ate_path = user_configuration_data["ATE_RESULT_PATH"][product_name.upper()]
            break
    
    # Navigating to the TPL folder of the case lot
    for file in os.listdir(product_ate_path):
        if test_program_name[-10:] in file:
            global tp_ate_path
            try:
                tp_ate_path = os.path.join(product_ate_path, file)
                tp_ate_path = os.path.join(tp_ate_path, 'TPL')

                # Find the BinDef file in
                bindef_path = navigating_to_bindef_file(tp_ate_path)
            except:
                return None

            return bindef_path