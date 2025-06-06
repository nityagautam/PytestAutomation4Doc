"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 5 Jun 2025
@last_modified: 06 Jun 2025
@desc: Utilities Class;
    Contains all the utilities for this automation framework.
"""


# Importing necessary libraries
import platform
import re


# Class: Utilities
class Utilities:
    def __init__(self):
        pass

    def is_windows(self):
        return re.search("Windows", platform.platform()) is not None

    def is_solaris(self):
        return re.search("SunOS", platform.platform()) is not None

    def is_mac(self):
        return re.search('Darwin', platform.platform()) is not None

    def is_linux(self):
        return re.search('Linux', platform.platform()) != None

    def get_os_platform(self):
        return platform.platform()

    def get_os_language(self):
        pass

    # File/Folder Operations
    # ----------------------------
    def create_folder(self, folder_path):
        import os
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return True
        return False
    
    def delete_folder(self, folder_path):
        import shutil
        import os
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            return True
        return False
    
    def create_file(self, file_path):
        import os
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write('')
            return True
        return False
    
    def delete_file(self, file_path):
        import os
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    
    def write_csv_file(self, file_path, data: list, mode: str = 'w'):
        import csv
        import os

        # Check if the file exists, if not create it
        if not os.path.exists(file_path):
            self.create_file(file_path)

        # Write data to the CSV file
        with open(file_path, mode=mode, newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        
    def get_all_files_in_folder(self, folder_path, file_ext: str = "html", resursive=False) -> list:
        import os
        import glob
        files: list = []

        # Check if the folder exists
        if os.path.exists(folder_path):
            if resursive:
                # Get all files in the folder and subfolders recursively
                files = glob.glob(os.path.join(folder_path, '**', f'*.{file_ext}'), recursive=True)
            else:
                # Get all files in the folder
                files = glob.glob(os.path.join(folder_path, f'*.{file_ext}'))
        
        # The provided folder does not exist
        else:
            print(f"\nFolder '{folder_path}' does not exist.")

        # Return the files in the folder
        return files
    
