import pandas as pd
import xlsxwriter

# Create a Pandas Excel writer using XlsxWriter as the engine.
# File Name: "Case_name_ATE_Class_Hot/Cold_"
# Row 0: Case Name
# Row 1: Current ATE - Class Hot Results
# Row 2: Unit# - Unit VID - Result - Bin - Description
# Row 3: Table
# Row 4: Original ATE - Class Hot Results
# Row 4: Unit# - Unit VID - Result - Bin - Description
# Row 6: Table
def writing_to_ate_excel_file(case_name, 
                              current_tp_df, 
                              original_tp_df, 
                              ate_class_type,
                              ate_excel_writer):
    # ate_result_df = pd.DataFrame({'A very long word qqqqqqqqqqqqqq': [10, 20, 30, 20, 15, 30, 45]})
    # case_name = "CI1234-1234666666666"

    # Initiate the Excel Writer engine
    # ate_excel_writer = pd.ExcelWriter(f'{case_name}_ATE_Result.xlsx', engine='xlsxwriter')


    # Feed the data to the Excel writer
    current_tp_df.to_excel(ate_excel_writer, sheet_name=f"{case_name} - {ate_class_type}", startrow=3, header=False, index=False)
    rows_jumped = current_tp_df['VID'].count()
    next_title_row = rows_jumped + 5
    next_start_row = rows_jumped + 6
    original_tp_df.to_excel(ate_excel_writer, sheet_name=f"{case_name} - {ate_class_type}", startrow=next_start_row+1, header=False, index=False)

    # Create an Excel workbook
    ate_workbook  = ate_excel_writer.book
    # Create an Excel worksheet with case_name title
    ate_worksheet = ate_excel_writer.sheets[f"{case_name} - {ate_class_type}"]

    # Add a header format.
    header_format = ate_workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'Center',
        'fg_color': '#D7E4BC',
        'border': 1,
        'font_size': 14})
    
    # Format the column width
    ate_worksheet.set_column('A:A', 10)
    ate_worksheet.set_column('B:D', 17)
    ate_worksheet.set_column('E:E', 240)

    # Format the title cell
    cell_format_title = ate_workbook.add_format()
    cell_format_title.set_bold()
    cell_format_title.set_font_size(18)
    cell_format_title.set_align('Center')
    # Format the content cell
    cell_format_content = ate_workbook.add_format()
    cell_format_content.set_font_size(12)

    # Merge two cells
    ate_worksheet.merge_range("A1:D1", "Merged Range")
    ate_worksheet.merge_range("A2:D2", "Merged Range")
    ate_worksheet.merge_range("A" + str(next_title_row + 1) + ":" + "D" + str(next_title_row + 1), "Merged Range")

    # Write the title 
    ate_worksheet.write(0, 0, case_name, cell_format_title)
    ate_worksheet.write(1, 0, f'Current {ate_class_type} TP Results', cell_format_title)
    ate_worksheet.write(next_title_row, 0, f'Original {ate_class_type} TP Results', cell_format_title )

    # Write the contents of the current class hot TP results
    for col_num, value in enumerate(current_tp_df.columns.values):
        ate_worksheet.write(2, col_num, value, header_format)
    
    for col_num, value in enumerate(original_tp_df.columns.values):
        ate_worksheet.write(next_title_row + 1, col_num, value, header_format)
    
    # Jumping to the row to write the Original TP result
    # Save the writing contents to the file
    # ate_excel_writer._save()

