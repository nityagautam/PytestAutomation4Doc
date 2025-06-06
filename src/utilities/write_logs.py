

from src.utilities.utilities import Utilities


def write_csv_logs_for_keyword_search(csv_log_file, data: list, mode: str='w'):
    """
    Write logs to a specified csv log file.

    Args:
        csv_log_file (str): The path to the log file.
        data (str): The data to write to the log file.
    """

    # Write the header first
    headers = data[0].keys() if data and isinstance(data[0], dict) else []
    # print(f">>> Writing headers: {headers} to {csv_log_file} in mode: {mode}")
    Utilities().write_text_file(csv_log_file, ", ".join(list(headers)), mode=mode)

    # Write the data rows
    for item in data:
        if not isinstance(item, dict):
            raise TypeError(f"Expected a list of data, but got {type(item)}. Please provide a list of lists.")
        
        row = [col[:80] if isinstance(col, str) and len(col) > 80 else str(col) for col in item.values()]
        # print(f">>> Writing row: {row}")
        Utilities().write_text_file(csv_log_file, ", ".join(list(row)), mode="a")
    
    print(f"Log written to {csv_log_file}")
