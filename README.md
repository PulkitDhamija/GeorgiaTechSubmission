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




This function, remove_empty_lines, takes a file path as input. It reads the content of the file specified by the given path in read mode ('r') and stores the lines in a list named lines.

Within the loop iterating over the lines, it checks if the line is empty and the previous line did not have content. If so, it continues to the next iteration, effectively skipping the empty line.

It also updates the previous_line_has_content flag to keep track of whether the current line has content or not.

Non-empty lines are appended to the new_lines list.

After processing all lines, the function overwrites the original file with the modified content, effectively removing consecutive empty lines.



This function, second_modification, accepts a file path as input along with an optional parameter max_length, which defaults to 100. It aims to modify the content of the file located at the specified path by splitting lines longer than the specified maximum length into multiple lines.

It begins by initializing an empty list named new_lines. Then, it opens the file specified by the given path in read mode ('r') and reads its contents into the list lines.

For each line in the file, the function checks if its length exceeds the max_length. If so, it splits the line into chunks of length max_length and appends each chunk to new_lines. Otherwise, it appends the entire line to new_lines.

After processing all lines, the function writes the modified content to a new file named "modified2.txt" by joining the lines in new_lines with newline characters between them. Finally, it returns the path to the modified file.



This function, third_modification, takes a file path as input. It reads the content of the file located at the specified path and stores the lines in a list named lines.

It then initializes an empty list new_lines to store the modified content.

The function iterates through each line in the file using a for loop with the index i. Within this loop, it sets a boolean variable keyword_found to False initially.

For each line, the function checks if any keyword from the keywords list is present in the line (case insensitive comparison). If a keyword is found, the function appends a slice of lines from i-2 to min(i+8, len(lines)) to new_lines to include the current line and lines before and after it within a certain range.

After processing all lines, the function writes the modified content to a new file named "modified3.txt". Finally, it returns the path to the modified file.



This function, `fourth_modification`, accepts a file path as input along with an optional parameter `chunk_size`, which defaults to 500. It aims to divide the content of the file located at the specified path into chunks of approximately equal size.

It begins by initializing an empty list named `chunks` to store the chunks of content. Then, it opens the file specified by the given path in read mode (`'r'`) and reads its contents into the list `lines`.

The function calculates the total number of lines in the file and determines the number of chunks required to split the content based on the specified `chunk_size`.

For each chunk, the function iterates through a range of indices corresponding to the start and end positions of the chunk within the list of lines. It extracts the lines within this range to form a chunk, joins them into a single string, and appends the resulting string to the `chunks` list.

After processing all chunks, the function returns the list of chunks containing the divided content.




This function, fifth_modification, takes a list of chunks as input along with an optional parameter max_chunk_size, which defaults to 10000. It aims to further split the chunks into smaller chunks if they exceed the specified maximum chunk size.

It initializes an empty list named new_chunks to store the modified chunks.

For each chunk in the input list chunks, the function checks if its length (after stripping leading and trailing whitespace) exceeds the max_chunk_size. If so, it calculates the number of splits required to divide the chunk into smaller chunks approximately equal to the max_chunk_size. Then, it iterates through the chunk and splits it into smaller chunks based on the calculated split size.

The resulting smaller chunks are appended to the new_chunks list. If a chunk does not exceed the max_chunk_size, it is directly appended to new_chunks without any further splitting.

After processing all chunks, the function returns the list of modified chunks containing either the original chunks or their smaller counterparts.




This response function generates responses based on the provided smaller chunks of text and the specified year. It iterates through each smaller chunk, generating a response using llm model based on a predefined prompt.

The prompt includes instructions to extract various pieces of information related to financial metrics for the given year. It also includes the chunk of text itself, enclosed within triple backticks (```), to provide context for the model.

For each chunk, the function generates a response using the model and appends it to a list of responses.

After processing all smaller chunks, the function joins the responses into a single string res. It then writes this string to a file named "first_response.txt".

Finally, it returns the path to the file containing the generated responses.



This function, removing_unnecessary_info, takes a file path as input. It reads the content of the file located at the specified path and stores the lines in a list named lines.

It initializes an empty list new_lines to store the modified content.

The function iterates through each line in the file using a for loop with the index i. Within this loop, it sets a boolean variable keyword_found to False initially.

For each line, the function checks if any word from the not_words list (presumably defined elsewhere in the code) is present in the line (case insensitive comparison). If such a word is found, it skips appending that line to new_lines.

After processing all lines, the function writes the modified content to a new file named "modified_response.txt". Finally, it returns the path to the modified file.


Thank you!!
