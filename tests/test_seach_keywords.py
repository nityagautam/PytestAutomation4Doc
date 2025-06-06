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
from src.utilities.write_logs import write_csv_logs_for_keyword_search


@pytest.mark.usefixtures("file_ext", "keyword_file")
def test_seach_keywords(file_list, file_ext, keyword_file):
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
        pytest -s tests/test_seach_keywords.py --keyword_file ./rules/keywords.txt --file_ext html --target_dir ./out
    """
    
    # Perform the Search / Find keywords for a file (given by the parameterized fixture in conftest.py)
    # ------------------------------
    print(f"\n\n>>> Given: Keyword file: {keyword_file}, Src file: {file_list} with file extension: {file_ext}\n")
    find_keyword = FindKeyword(src_file=file_list, keywords_file=keyword_file, file_ext=file_ext, verbose=False)
    issue_counter, data = find_keyword.find()
    
    # Write the data to a CSV file
    # ------------------------------
    csv_file_path = os.path.abspath("./out/find_keyword_issues.csv")
    write_csv_logs_for_keyword_search(csv_log_file=csv_file_path, data=data, mode='w')
    
    # Assert now
    # ------------------------------
    if issue_counter > 0:
        print(f"Keyword found in file: {file_list}")
        print(f"Data: {data}")
        pytest.fail(f"Keyword found in file: {file_list} with issues: {issue_counter}")
    else:
        print(f"No keyword found in file: {file_list}")
        assert issue_counter == 0

    """
    Data: [
        {
        'file': './out/sample copy 3.pdf', 
        'page': 1, 
        'line': 2, 
        'sentence': 'Part A-GEN GENERAL (A1) First Name RUCHI (A2)Middle Name J (A3) Last Name TIWARI (A4) PAN AXEPT4723G (A6) Flat/Door/Block No. B-109, Jai Sai Pooja Apt., (A7) Name of Premises/Building/Village (A5) Status (Tick) Individual HUF (A8) Road/Street/Post Office Jain Nagar, Navghar Road (A14) Date of Birth/ Formation (DD/MMM/YYYY) 02-Jul-1995 (A9) Area/locality Bhayander(E) (A15) Aadhaar Number (12 digit) / Aadhaar Enrolment Id (28 digit) (if eligible for Aadhaar) 6xxx xxxx 3688 (A11) State 19 - Maharashtra (A10) Town/City/District Thane (A12) Country/Region 91 - India (A13) Pin code/Zip code 401105 (A16) Residential/Office Phone Number with STD/ISD code Mobile No. 1 918976921206 (A17) Mobile No. 2 (A18) Email Address-1(self) ruchitiwari400@gmail.com (A19) Email Address-2 (a1i) Filed u/s (Tick)[Please see instruction ] 139(1)-On or before due date, 139(4)-After due date, 139(5)-Revised Return, 92CD-Modified return, 139(9A) / 119(2)(b)- After condonation of delay, 139(8A) - Updated return (A20) (a1ii) Or Filed in response to notice u/s 139(9), 142(1), 148 (a2) Are you opting for new tax regime u/s 115BAC?'}, {'file': './out/sample copy 3.pdf', 'page': 37, 'line': 138, 'sentence': 'Year in which deduc ted TDS b/f Deducted in own hands Deducted in the hands of spouse as per section 5A or any other person as per rule 37BA(2) (if applicable) Claimed in own hands Claimed in the hands of spouse as per section 5A or any other person as per rule 37BA(2) (if applicable) Gross Amount Head of Income TDS credit being carried forward (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) (11) (12) (13) Income TDS Income TDS PAN/Aadhaar TDS claimed in own hands (total of column 9) 0 Note:Please enter total of column 9 in 15b of Part B- TTI E Details of Tax Collected at Source (TCS) [As per Form 27D issued by Collector(s)] SI.No. Tax Deduction and Collection Account Number of the Collector Name of the Collector Tax Collected Amount out of (4) being claimed Amount out of (4) being claimed in the hands of spouse, if section 5A is applicable (1) (2) (3) (4) (5) (6) TCS being claimed this year (total of column 5) 0 Note:Please enter total of column (5) in 15c of Part B-TTI xyz xyz VERIFICATION xyz I, RUCHI J TIWARI son/ daughter of JAYRAM TIWARI solemnly declare that to the best of my knowledge and belief, the information given in the return and schedules thereto is correct and complete and is in accordance with the provisions of the Income-tax Act, 1961.'}]
    """