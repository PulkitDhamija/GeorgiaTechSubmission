# GeorgiaTechSubmission

I will update the readme file by 10th May 11:59 pm EST with all the description and video of the app and the repository with the final code and app code.

Description:

Problem Statement:

Approach:

Code explanation:

The code initializes a downloader object named dl for the company "MyCompanyName" with the email address "my.email@domain.com". Then, it defines a list of equity IDs, including "WMT", "MSFT", and "AAPL". It iterates over each equity ID in the list and uses the downloader object dl to fetch the 10-K filings for the corresponding company. The filings are retrieved for the period after December 31, 2020, and before December 31, 2023. Additionally, the parameter download_details is set to False, indicating that only the filings themselves are being downloaded without any additional details.

This code snippet processes the 10-K filing directories for the company "MSFT" (Microsoft) located at the specified folder path. It initializes a regular expression pattern r'-(\d+)-' to match the year in the folder names. It then creates an empty list named years to store the extracted years. The code iterates through each folder in the specified directory using os.listdir(folder_path). For each folder, it constructs the full path using os.path.join(folder_path, folder_name). If the path corresponds to a directory (os.path.isdir(full_path)), it attempts to match the pattern in the folder name using re.search(pattern, folder_name). If a match is found, it extracts the year from the folder name using match.group(1) and renames the folder to just the year. Finally, it appends the extracted year to the years list.

This snippet aims to collect file paths for the 10-K filings of Microsoft (MSFT) stored in the specified directory (sec-edgar-filings/MSFT/10-K). It initializes an empty dictionary named file_paths to store the file paths along with their corresponding years.

The code iterates through each year in the years list (presumably extracted in a previous step). For each year, it constructs the full path to the corresponding directory using os.path.join(folder_path, folder_name).

The path is then appended with a trailing '/' to ensure it represents a directory. If the directory exists (os.path.exists(full_path)) and is not empty (files), the code retrieves the list of files in that directory using os.listdir(full_path).

If files are found, it selects the first file (files[0]) and constructs the full path to that file. This full path, along with the corresponding year (converted to an integer), is added to the file_paths dictionary.

This function, named first_modification, takes a file path as input. It opens the file specified by the given path in read mode ('r') and reads its contents line by line.

Within the loop iterating over the lines, several checks and modifications are performed:

It removes content between < and > using regular expressions.
It skips lines containing certain special characters or whitespace patterns.
It detects if the line contains references to certain file types like images (.jpg), Excel files (.xlsx), zip archives (.zip), or HTML files (.htm).
It filters out lines related to detected file types to avoid processing them further.
It appends the filtered lines to a list named new_lines.
After processing all lines, the function writes the filtered content to a new file named 'modified1.txt' and returns the path to the modified file.



Thank you!!
