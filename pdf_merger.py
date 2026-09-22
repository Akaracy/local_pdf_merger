import PySimpleGUI as sg
import PyPDF2
import os 
from pathlib import Path

"""-------------------------------FUNCTION----------------------------"""
def merge_pdf(files, output_folder_path, name):
    if files:
        merger = PyPDF2.PdfMerger()
        for file in files:
            if is_valid_path(file):
                merger.append(file)
        
        output_path = os.path.join(output_folder_path, f'{name}.pdf')
        with open(output_path, "wb") as output_pdf:
            merger.write(output_pdf)
            print("merged!!!")
        sg.popup_no_titlebar("PDF succesfully merged")
    sg.popup_no_titlebar("No files to merge")
        
    
"""-----------------EXCEPTION FUNCTION--------------------------------------"""
def is_valid_path(filepath):
    if filepath and os.path.exists(filepath):
        return True
    sg.popup_no_titlebar(f"File {filepath} does not exist")
    return False

"""-------------------------------GUI----------------------------"""

files_to_merge = []

list_box = sg.Listbox(files_to_merge,
                    size=(30,4),
                    expand_y = True,
                    enable_events = True,
                    key = 'file_list'
                    )

def main_window():
    # Define the window's contents
    layout = [[sg.Text("PDF to merge")],
            [sg.Text("Input Files : "), sg.Input(key='-IN-'), sg.FileBrowse(file_types=(("PDF", "*.pdf*"),)), sg.Button("Add2Merge")],
            [list_box],
            [sg.Text("Output Folder : "), sg.Input(key='-OUT-'), sg.FolderBrowse()],
            [sg.Text("Name of the new PDF : ")],
            [sg.Input(key= '-NAME-')],
            [sg.Button('Merge')]]

    # Create the window
    window = sg.Window('Local PDF Merger', layout)

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED :
            break
        if event == 'Add2Merge':
            files_to_merge.append(values['-IN-'])
            print(files_to_merge)
            window['file_list'].update(files_to_merge)
        if event == 'Merge':
            if is_valid_path(values['-OUT-']):
                merge_pdf(files_to_merge, values['-OUT-'], values['-NAME-'])

    # Finish up by removing from the screen
    window.close()



"""-------------------------------MAIN----------------------------"""
if __name__ == "__main__":
    SETTINGS_PATH = Path.cwd()
    # create the settings object and use ini format
    settings = sg.UserSettings(
        path=SETTINGS_PATH, filename="config.ini", use_config_file=True, convert_bools_and_none=True
    )
    theme = settings["GUI"]["theme"]
    font_family = settings["GUI"]["font_family"]
    font_size = int(settings["GUI"]["font_size"])
    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))
    
    main_window()


# test = ['/home/akara/Fun/pdf_merger/data/1.pdf', '/home/akara/Fun/pdf_merger/data/1.pdf']
# merge_pdf(test, '/home/akara/Fun/pdf_merger/data', 'test')