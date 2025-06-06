"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 5 Jun 2025
@last_modified: 06 Jun 2025
@desc: pytest test to search for keywords in files with a specific extension.
@note: This test will fail if any keyword is found in the files.
    
Args:
    file_list (list): List of files to search for keywords. 
                    [this is a (parameterized) fixture that provides the list of files 
                    from the target directory with given extensions for tests.]
    file_ext (str): The file extension to filter files by.
Raises:
    AssertionError: If any keyword is found in the files.
Example:
    pytest -s tests/test_seach_keywords.py --file_ext html --target_dir ./out
"""


import os
import pytest
from src.core.find_keyword import FindKeyword
from src.utilities.utilities import Utilities


def test_seach_keywords(file_list, file_ext):
    """
    Test to search for keywords in files with a specific extension in the target directory.
    This test will fail if any keyword is found in the files.
    
    Args:
        file_list (list): List of files to search for keywords. 
                        [this is a (parameterized) fixture that provides the list of files 
                        from the target directory with given extensions for tests.]
        file_ext (str): The file extension to filter files by.
    Raises:
        AssertionError: If any keyword is found in the files.
    Example:
        pytest -s tests/test_seach_keywords.py --file_ext html --target_dir ./out
    """
    
    # Perform the Search / Find keywords for a file (given by the parameterized fixture in conftest.py)
    # ------------------------------
    find_keyword = FindKeyword(src_file=file_list, keywords_file=os.path.abspath("./rules/keywords.txt"), file_ext=file_ext, verbose=True)
    issue_counter, data = find_keyword.find()

    # Write the data to a CSV file
    # ------------------------------
    csv_file_path = os.path.abspath("./out/find_keyword_issues.csv")
    Utilities().write_csv_file(file_path=csv_file_path, data=data, mode='w')
    print(f"Log written to : {csv_file_path}")

    # Assert now
    # ------------------------------
    if issue_counter > 0:
        print(f"Keyword found in file: {file_list}")
        print(f"Data: {data}")
        pytest.fail(f"Keyword found in file: {file_list} with issues: {issue_counter}")
    else:
        print(f"No keyword found in file: {file_list}")
        assert issue_counter == 0
