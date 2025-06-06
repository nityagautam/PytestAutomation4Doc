# PytestAutomation4Doc
Pytest automation for the documentation testing

- Keyword search in document file with follwing extension
    - PDF
    - HTML
    - TXT

> Usecase: Lets say we want to find that any document shall not have older build no anywhere in the document. Etc...

- TODO: Spelling and Grammer Check for documents with following extension
    - HTML
    - PDF


### Pre-Requisite:
<pre>
    1. python3
</pre>

### Setup
<pre>
    1. Clone the repo
        ~ git clone {this_repo_link}
        ~ cd ./PytestAutomation4Doc
    2. Run the requirement (You can also create virtualenv first before installing modules)
        ~ pip install -r requirements.txt
</pre>


### Execution
> `python3 -m pytest` {runs the entire framework test}

> `python3 -m pytest <PATH_TO_TEST_FILE> [ARGS]` {runs the specific test file}

<br/>

Example: 
> `pyton3 -m pytest -s tests/test_seach_keywords.py --file_ext html --target_dir ./out`

> `pyton3 -m pytest -s tests/test_seach_keywords.py --file_ext pdf --target_dir ./out`

> `pyton3 -m pytest -s tests/test_seach_keywords.py --file_ext txt --target_dir ./out`

> `pyton3 -m pytest -s tests/test_seach_keywords.py --file_ext pdf --target_dir ./out --keyword_file ./rules/keywords.txt`


Output:
![SampleExecution](out/screenshots/execution-sample-2.png)


### Folder Structure
<pre>
      root
        |____ out
                |____ screenshots
                |____ test_report.html <-- pytest html report
                |____ test_result.xml  <-- JUnit report
        |____ rules
                |____ keywords.txt
                |____ ...
        |____ src
                |____ core
                        |____ find_keyword.py
                        |____ todo_future_py...
                |____ config
                        |____ config.py (Contains the configuration for entire framework)[HP]
                |____ utilities
                        |____ 
                        |____ Utilities.py (Common Utility)
                |____ __init__.py
        |____ tests
                |____ test_*.py
                |____ ...
        |____ conftest.py (Contains pytest common fixtures)
        |____ LICENSE
        |____ pytest.ini (Contains pytest configuration)
        |____ README.md
        |____ requirements.txt (Python lib/modules requirements)
</pre>
