# working greate 20249405 2205 but without choosing the file types


import os
import pandas as pd
import fitz  # PyMuPDF, ensure this is installed as it's not standard
from datetime import datetime
import xlsxwriter
import tkinter as tk
from tkinter import filedialog

# Constants for unchanging parameters, adhering to uppercase naming
PDF_EXTENSION = "*.pdf"
EXCEL_SHEET_NAME = 'PDF Files Info'
COLUMN_WIDTH = 30
HEADER_BG_COLOR = '#D7E4BC'

# New dynamic file name with date and time
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
EXCEL_FILE_NAME = f'Files_list_{current_time}.xlsx'


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def get_file_info(pdf_path):
    """
    Retrieves and formats creation and modification time of a file.
    """
    creation_time = os.path.getctime(pdf_path)
    mod_time = os.path.getmtime(pdf_path)
    return (
        datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d'),
        datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
    )


def apply_excel_designs(writer, df):
    """
    Applies formatting designs to the Excel file being written.
    """
    workbook = writer.book
    worksheet = writer.sheets[EXCEL_SHEET_NAME]
    header_format = workbook.add_format({
        'bold': True, 'valign': 'top', 'fg_color': HEADER_BG_COLOR, 'border': 1,
        'align': 'right'  # Right-align header for Hebrew text
    })
    cell_format = workbook.add_format({'align': 'right'})  # Right-align cells for Hebrew text
    worksheet.write_row('A1', df.columns, header_format)
    worksheet.set_column('A:E', COLUMN_WIDTH, cell_format)  # Apply cell_format to all cells


def add_creation_note(writer, df):
    """
    Adds a creation note in a cell at the end of the data with a hyperlink.
    """
    workbook = writer.book
    worksheet = writer.sheets[EXCEL_SHEET_NAME]
    next_row = len(df) + 2  # Adjust row position as needed

    hyperlink_url = 'https://www.linkedin.com/in/keren-drevin/'
    hyperlink_format = workbook.add_format({'color': 'blue', 'underline': 1})
    worksheet.write_url(next_row, 0, hyperlink_url, hyperlink_format, "Created by Keren Drevin, Visit my Linkedin page")


def choose_directory():
    """
    Opens a dialog for directory selection, ensuring it appears on top.
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    selected_directory = filedialog.askdirectory()
    root.destroy()  # Clean-up Tkinter root window
    return selected_directory


def main():
    """
    Orchestrates PDF extraction and Excel file creation based on the user-selected directory.
    """
    selected_directory = choose_directory()
    if not selected_directory:
        print("Directory selection was cancelled.")
        return

    # Extract the last part of the selected_directory path, which is the directory name
    directory_name = os.path.basename(os.path.normpath(selected_directory))

    # Format the current date and time
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M')

    # Incorporate the directory name and current date and time into the Excel file name
    EXCEL_FILE_NAME = f'{directory_name}_Files_list_{current_time}.xlsx'

    # Continue with your script...
    excel_file_path = os.path.join(selected_directory, EXCEL_FILE_NAME)

    excel_file_path = os.path.join(selected_directory, EXCEL_FILE_NAME)
    data_columns = ['Directory Name', 'PDF File Name', 'Creation Date', 'Modification Date', 'Text Snippet']
    data = {col: [] for col in data_columns}

    for root, _, files in os.walk(selected_directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                pdf_name = os.path.basename(pdf_path)
                directory_name = os.path.basename(root)
                creation_time, mod_time = get_file_info(pdf_path)
                text_snippet = extract_text_from_pdf(pdf_path)[:100]
                data_row = [directory_name, pdf_name, creation_time, mod_time, text_snippet]

                for col_name, value in zip(data_columns, data_row):
                    data[col_name].append(value)

    df = pd.DataFrame(data)
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=EXCEL_SHEET_NAME, index=False)
        apply_excel_designs(writer, df)
        add_creation_note(writer, df)  # Add the creation note with a hyperlink

    print(f"Excel file '{excel_file_path}' has been created.")


if __name__ == "__main__":
    main()

