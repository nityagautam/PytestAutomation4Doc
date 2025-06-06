"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 5 Jun 2025
@last_modified: 06 Jun 2025
@desc: FindKeyword Class;
    This class is used to find keywords in files with specific extensions (HTML, PDF, TXT).
@note: This class will return the count of issues found and the relevant data.
"""


import re
from bs4 import BeautifulSoup
import fitz


class FindKeyword:
    def __init__(self, src_file: str, keywords_file: str, file_ext: str = "html", verbose: bool = False):
        self.src_file = src_file
        self.file_ext = file_ext
        self.keywords_file = keywords_file
        self.keywords = []
        self.verbose = verbose
        self.issues = []
        self.data = {}

        # Load keywords from the specified file
        self.load_keywords()

        if self.verbose:
            print(f"Initialized FindKeyword with keyword file: {self.keywords}")
        
        
    def load_keywords(self):
        """Load keywords from a file."""
        try:
            # Read the keyword from the file, assuming one keyword per line
            with open(self.keywords_file, 'r') as file:
                self.keywords = [keyword.strip() for keyword in file.readlines()]

        except FileNotFoundError as e:
            if self.verbose:
                print(f"Keyword file '{self.keywords_file}' not found.\nRefer: {e}\n")
            else:
                print(f"Keyword file '{self.keywords_file}' not found. Please check again.")

    def find(self) -> any:
        """Check if the keyword is present in the text."""
        if self.file_ext == "html":
            return self.__find_keyword_in_html()
        elif self.file_ext == "pdf":
            return self.__find_keyword_in_pdf()
        elif self.file_ext == "txt":
            return self.__find_keyword_in_txt()
        else:
            if self.verbose:
                print(f"Unsupported file extension: {self.file_ext}")
            return False
        

    def __find_keyword_in_html(self) -> tuple:
        """Find keyword in HTML content."""
        file_data = []
        issue_counter = 0
        line_counter = 1
        page_soup = None

        try:
            # process the HTML file with beautifulsoup
            with open(self.src_file, 'rb') as file:
                page_soup = BeautifulSoup(file, 'html.parser')
                
            # extract text from the HTML content
            page_title = page_soup.title.text if page_soup.title else "No Title"
            page_sentences = re.split(r'(?<!\W\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', page_soup.text)

            # Iterate through each sentence in the HTML content
            for sentence in page_sentences:
                sentence = " ".join(s.strip() for s in sentence.splitlines())

                # Iterate through each keyword and check if it is present in the sentence
                for keyword in self.keywords:

                    # Check if the keyword is present in the sentence; Consider lower case always
                    if keyword.lower() in sentence.lower():
                        issue_counter += 1
                        file_data.append({
                            "file": self.src_file,
                            "title": page_title.strip(),
                            "line": line_counter,
                            "sentence": sentence
                        })

                # Increment the line counter for each sentence processed
                line_counter += 1

        except Exception as e:
            if self.verbose:
                print(f"Error reading HTML file {self.src_file}: {e}")
            return -1, file_data
        
        # Return the Collected data
        return issue_counter, file_data
    
    def __find_keyword_in_pdf(self) -> tuple:
        """Find keyword in PDF content."""
        file_data = []
        issue_counter = 0
        line_counter = 1

        try:
            # Open the PDF file using PyMuPDF (fitz)
            # Note: fitz is the PyMuPDF library, which allows for PDF manipulation
            # Ensure that the file exists and is a valid PDF
            pdf_doc = fitz.open(self.src_file)

            # Iterate through each page in the PDF document
            for page_num in range(len(pdf_doc)):

                page = pdf_doc[page_num]
                page_text = page.get_text("text")

                # Split the text into sentences
                page_sentences = re.split(r'(?<!\W\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', page_text)

                # Iterate through each sentence in the PDF content
                for sentence in page_sentences:
                    sentence = " ".join(s.strip() for s in sentence.splitlines())

                    # verbose mode: print the current page and sentence being processed
                    if self.verbose:
                        print(f"Processing Page {page_num + 1}, Line {line_counter}: {sentence}")

                    # Iterate through each keyword and check if it is present in the sentence
                    for keyword in self.keywords:

                        # Check if the keyword is present in the sentence; Consider lower case always
                        if keyword.lower() in sentence.lower():
                            issue_counter += 1
                            file_data.append({
                                "file": self.src_file,
                                "page": page_num + 1,  # Page numbers are 1-indexed
                                "line": line_counter,
                                "sentence": sentence
                            })

                    # Increment the line counter for each sentence processed
                    line_counter += 1

            # Close the PDF document
            pdf_doc.close()

        except fitz.FileDataError as e:
            if self.verbose:
                print(f"Error reading PDF file {self.src_file}: {e}")
            return -1, file_data

        # Return the Collected data
        return issue_counter, file_data
    
    def __find_keyword_in_txt(self) -> tuple:
        # TODO: Does not work fully yet, need to enhance it further
        """
        Find keyword in text content.
        This method reads a text file, checks each line for the presence of keywords,
        and returns the count of issues found along with the relevant data.
        Returns:
            tuple: A tuple containing the count of issues found and a list of dictionaries
                   with file name, line number, and sentence where the keyword was found.
        If an error occurs while reading the file, it returns -1 and an empty list.
        Example:
            >>> find_keyword = FindKeyword(src_file='example.txt', keywords_file='keywords.txt')
            >>> issue_count, data = find_keyword.__find_keyword_in_txt()
            >>> print(issue_count)  # Number of issues found
            >>> print(data)  # List of dictionaries with file, line, and sentence information
        Note:
            - The method assumes that the text file is encoded in UTF-8.
            - It skips empty lines and only processes non-empty lines.
            - The line number is set to 1 for the entire text file since it is treated as a single block of text.
        
        """
        issue_counter = 0
        line_counter = 1
        file_data = []
        contents = None

        try:
            with open(self.src_file, 'r', encoding='utf-8') as file:
                contents = file.readlines()
                
            for content in contents:
                content = content.strip()
                
                # Skip empty lines
                if not content:
                    continue

                # Iterate through each keyword and check if it is present in the content
                for keyword in self.keywords:
                    
                    if keyword.lower() in content.lower():
                        issue_counter += 1
                        file_data.append({
                            "file": self.src_file,
                            "line": 1,  # For text files, we can assume line 1 since it's a single block of text
                            "sentence": content.strip()
                        })
                # Increment the line counter for each line processed
                line_counter += 1

        except Exception as e:
            if self.verbose:
                print(f"Error reading text file {self.src_file}: {e}")
            return -1, file_data
        
        # Return the Collected data
        return issue_counter, file_data 
    


if __name__ == "__main__":
    # HTML Example usage of the FindKeyword class
    # find_keyword = FindKeyword(src_file="./out/report.html", keywords_file="keywords.txt", file_ext="html", verbose=True)
    # issue_count, data = find_keyword.find()
    # print(f"Issue Count: {issue_count}")
    # print(f"Data: {data}")

    # PDF Example usage of the FindKeyword class
    find_keyword_pdf = FindKeyword(src_file="./out/sample.pdf", keywords_file="./rules/keywords.txt", file_ext="pdf", verbose=True)
    issue_count_pdf, data_pdf = find_keyword_pdf.find()
    print(f"Issue Count PDF: {issue_count_pdf}")
    print(f"Data PDF: {data_pdf}")
