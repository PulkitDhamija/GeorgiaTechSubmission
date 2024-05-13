# GeorgiaTechSubmission

I will update the readme file by 10th May 11:59 pm EST with all the description and video of the app and the repository with the final code and app code.

Problem Statement: To extract the information from 10-K fillings of companies and generate insights using LLM models.

Description: My ultimate aim is to extract information like earnings per share, revenue, gross margin, current assets, etc., from 10-K sec edgar fillings and generate insights based on yearly changes from 1995-2023.

Challenges: 

- Unable to parse XBRL files using already available parsers in Python.
- Without parsers, unable to remove unnecessary information from the file text.
- Even after removing unnecessary information like HTML tags and other styling content, a large amount of text was still left to be processed by the LLM model to generate insights.
- This large amount of text was also not clean.
- Even after giving the LLM model the necessary information, the LLM model was unable to extract the "said" information from the text with good accuracy.

Approach:

- Cleaning the text as much as possible manually.
- Give this text to the LLM model, such that it can give me the relevant "said" financial information from the text.
- Idea is to reduce the text as much as possible which has to be processed by the LLM model to extract the "said" information.
- For this, I applied various modifications, which included:
    -  Finding lines with relevant content like earnings per share, income, etc. (stored in variable 'keywords' in the code) and storing the previous two and next eight lines from that line.
    -  In some texts, only one line had a large amount of text, so to tackle this, I put a cap of 100 words per line using the "second modification" function (explained below in the code explanation).
    -  After getting these relevant lines and storing them in text, I divided this text into chunks of 500 lines.
    -  Now, after dividing into chunks of 500 lines, some chunks contained a large amount of text, so to tackle this, I put a cap of 10000 words per chunk using the "fifth modification" function.
    - Gave these chunks to the LLM model, extracted the "said" relevant information, and aggregated this information by again passing the response (which was modified manually to remove unnecessary information) to the LLM model.
    -  Did this for each year and extracted the relevant information for each year's 10-K filings.
    -  Finally, aggregated the information for all years and gave that to the LLM model to generate insights.
- Developed a streamlit app to showcase the insights, which takes input as a ticker, downloads the relevant sec-edgar fillings and generates insights using the LLM model.

## Code explanation:

Downloading sec files code cell:

The code initializes a downloader object named dl for the company "MyCompanyName" with the email address "my.email@domain.com". Then, it defines a list of equity IDs, including "WMT", "MSFT", and "AAPL". It iterates over each equity ID in the list and uses the downloader object dl to fetch the 10-K filings for the corresponding company. The filings are retrieved for the period after December 31, 1994, and before December 31, 2023. Additionally, the parameter download_details is set to False, indicating that only the filings themselves are being downloaded without any additional details.


Code to change the name of the files:

The code processes the 10-K filing directories for the company "MSFT" (Microsoft) located at the specified folder path. It initializes a regular expression pattern r'-(\d+)-' to match the year in the folder names. It then creates an empty list named years to store the extracted years. The code iterates through each folder in the specified directory using os.listdir(folder_path). For each folder, it constructs the full path using os.path.join(folder_path, folder_name). If the path corresponds to a directory (os.path.isdir(full_path)), it attempts to match the pattern in the folder name using re.search(pattern, folder_name). If a match is found, it extracts the year from the folder name using match.group(1) and renames the folder to just the year. Finally, it appends the extracted year to the `years` list.


To get all the file paths and hash them with their respective year:

This code aims to collect file paths for the 10-K filings of Microsoft (MSFT) stored in the specified directory (sec-edgar-filings/MSFT/10-K). It initializes an empty dictionary named `file_paths` to store the file paths along with their corresponding years.\
The code iterates through each year in the `years` list (presumably extracted in a previous step). For each year, it constructs the full path to the corresponding directory using os.path.join(folder_path, folder_name).\
The path is then appended with a trailing '/' to ensure it represents a directory. If the directory exists (os.path.exists(full_path)) and is not empty (files), the code retrieves the list of files in that directory using os.listdir(full_path).\
If files are found, it selects the first file (files[0]) and constructs the full path to that file. This full path, along with the corresponding year (converted to an integer), is added to the `file_paths` dictionary.


Function to remove empty lines (it will used after every modification):

This function, `remove_empty_lines`, takes a file path as input. It reads the content of the file specified by the given path in read mode ('r') and stores the lines in a list named lines.
Within the loop iterating over the lines, it checks if the line is empty and the previous line does not have content. If so, it continues to the next iteration, effectively skipping the empty line.\
It also updates the `previous_line_has_content` flag to keep track of whether the current line has content or not.\
Non-empty lines are appended to the `new_lines` list.\
After processing all lines, the function overwrites the original file with the modified content, effectively removing consecutive empty lines.


First modification:

This function, named `first_modification`, takes a file path as input. It opens the file specified by the given path in read mode ('r') and reads its contents line by line.\
Within the loop iterating over the lines, several checks and modifications are performed:\

It removes content between < and > using regular expressions.\
It skips lines containing certain special characters or whitespace patterns.\
It detects if the line contains references to certain file types like images (.jpg), Excel files (.xlsx), zip archives (.zip), or HTML files (.htm).\
It filters out lines related to detected file types to avoid processing them further.\
It appends the filtered lines to a list named `new_lines`.\
After processing all lines, the function writes the filtered content to a new file named `modified1.txt` and returns the path to the modified file.


Second modification:

This function, `second_modification`, accepts a file path as input along with an optional parameter `max_length`, which defaults to `100`. It aims to modify the content of the file located at the specified path by splitting lines longer than the specified maximum length into multiple lines.\
It begins by initializing an empty list named `new_lines`. Then, it opens the file specified by the given path in read mode ('r') and reads its contents into the list lines.\
For each line in the file, the function checks if its length exceeds the `max_length`. If so, it splits the line into chunks of length `max_length` and appends each chunk to `new_lines`. Otherwise, it appends the entire line to `new_lines`.\
After processing all lines, the function writes the modified content to a new file named `modified2.txt` by joining the lines in `new_lines` with newline characters between them. Finally, it returns the path to the modified file.

Third modification:

This function, `third_modification`, takes a file path as input. It reads the content of the file located at the specified path and stores the lines in a list named lines.\
It then initializes an empty list, `new_lines`, to store the modified content.\
The function iterates through each line in the file using a for loop with the index i. Within this loop, it sets a boolean variable `keyword_found` to False initially.\
For each line, the function checks if any keyword from the keywords list is present in the line (case-insensitive comparison). If a keyword is found, the function appends a slice of lines from i-2 to min(i+8, len(lines)) to `new_lines` to include the current line and lines before and after it within a certain range.\
After processing all lines, the function writes the modified content to a new file named `modified3.txt`. Finally, it returns the path to the modified file.

Fourth modification:

This function, `fourth_modification`, accepts a file path as input along with an optional parameter `chunk_size`, which defaults to `500`. It aims to divide the content of the file located at the specified path into chunks of approximately equal size.\
It begins by initializing an empty list named `chunks` to store the chunks of content. Then, it opens the file specified by the given path in read mode ('r') and reads its contents into the list `lines`.\
The function calculates the total number of lines in the file and determines the number of chunks required to split the content based on the specified `chunk_size`.\
For each chunk, the function iterates through a range of indices corresponding to the start and end positions of the chunk within the list of lines. It extracts the lines within this range to form a chunk, joins them into a single string, and appends the resulting string to the `chunks` list.\
After processing all chunks, the function returns the list of chunks containing the divided content.


Fifth modification:

This function, `fifth_modification`, takes a list of chunks as input along with an optional parameter `max_chunk_size`, which defaults to `10000`. It aims to further split the chunks into smaller chunks if they exceed the specified maximum chunk size.\
It initializes an empty list named new_chunks to store the modified chunks.\
For each chunk in the input list chunks, the function checks if its length (after stripping leading and trailing whitespace) exceeds the `max_chunk_size`. If so, it calculates the number of splits required to divide the chunk into smaller chunks approximately equal to the `max_chunk_size`. Then, it iterates through the chunk and splits it into smaller chunks based on the calculated split size.\
The resulting smaller chunks are appended to the `new_chunks` list. If a chunk does not exceed the `max_chunk_size`, it is directly appended to `new_chunks` without any further splitting.\
After processing all chunks, the function returns the list of modified chunks containing either the original chunks or their smaller counterparts.


`response` function:

This response function generates responses based on the provided smaller chunks of text and the specified year. It iterates through each smaller chunk, generating a response using the LLM model based on a predefined prompt.\
The prompt includes instructions to extract various pieces of information related to financial metrics for the given year. It also includes the chunk of text itself, enclosed within triple backticks (```), to provide context for the model.\
For each chunk, the function generates a response using the model and appends it to a list of responses.\
After processing all smaller chunks, the function joins the responses into a single string res. It then writes this string to a file named `first_response.txt`.\
Finally, it returns the path to the file containing the generated responses.

`removing_unnecessary_info` function:

This function, `removing_unnecessary_info`, takes a file path as input. It reads the content of the file located at the specified path and stores the lines in a list named lines.\
It initializes an empty list, `new_lines`, to store the modified content.\
The function iterates through each line in the file using a for loop with the index i. Within this loop, it sets a boolean variable `keyword_found` to False initially.\
For each line, the function checks if any word from the not_words list is present in the line (case insensitive comparison). If such a word is found, it skips appending that line to `new_lines`.\
After processing all lines, the function writes the modified content to a new file named `modified_response.txt`. Finally, it returns the path to the modified file.

`final_aggregate_response` function:

After removing lines that contain words like `not` from the first response of the LLM model, I again passed it to the LLM model to summarize all the information it has.

This final_aggregate_response function aggregates the financial information contained in a file specified by the input path.\
It begins by reading the content of the file located at the specified path using with open(path, 'r') as file, and stores the content in the variable `res`.\
Then, it constructs a prompt string that instructs to aggregate various financial information items. The prompt includes the content of the file enclosed within triple backticks (```) to provide context for the model.\
After constructing the prompt, the function generates a response using the LLM model based on the prompt.\
Finally, it returns the generated response text.

Final steps:

`all_year_response` code cell:

This code snippet iterates through a list of years, presumably corresponding to financial filings. For each year, it prepares the associated file path and adjusts the year format if necessary. The code then conducts a sequence of data manipulations and processing steps on the financial filing data. These steps involve various modifications, such as removing unnecessary content, splitting the data into smaller manageable chunks, generating responses based on these chunks, and aggregating the responses. Each manipulation step is called sequentially, with the output of one step being fed into the next. Progress is printed out, indicating the year being processed and the number of data chunks generated for that year. Finally, the responses generated for each year are stored in a dictionary for further analysis or use.

Finally, aggregated the output of the above cell and gave that as input to the LLM model to generate insights.


## Example

I ran the code for the year 2021 10-K file of MSFT, and extracted the relevant information using the LLM model and this was the output:
~~~
**2021**

**Shares Purchased and Average Price Paid per Share/Number of Shares Purchased**


**Total Net Sales and Year Change/Net Sales**

- Total net sales: $168,088 
- Year change/net sales: 18%

**Total Gross Margin and Total Gross Margin Percentage/Total Cost of Sales/Gross Margin/Gross Margin Percentage**

- Total gross margin: $59,774
- Total gross margin percentage: 36%
- Total cost of sales: $108,314
- Gross margin: $59,774


**Net Income/Total Net Income**

- Net income: $61,271

**Earnings Per Share**

- Diluted earnings per share: $8.05

**Total Current Assets/Current Assets**

- Total current assets: $184,406
- Current assets: $18,4406

**Total Shareholders’ Equity/Shareholders’ Equity**


**Total Current Liabilities/Current Liabilities**

- Total current liabilities: $88,657
- Current liabilities: $88,657

**Period End**

- June 26, 2022

**Total Revenue/Revenue**

- Total revenue: $168,088
**2020**

 - Net income/total net income: $61,271
 - Total current assets/current assets: $184,406
 - Total current liabilities/current liabilities: $88,657
 - Period end: Jun. 30, 2020
~~~

Then I did this for every year and aggregated it, gave it the LLM model to generate insights and this was the output:
~~~
**Insights:**

**Revenue:** MSFT's total net sales have grown significantly over the years, from $5,937 million in 1995 to $198,270 million in 2022, representing a remarkable increase of over 3,200%. This consistent growth indicates the company's ability to expand its market reach and generate increasing revenue streams.

**Net income:** MSFT's net income has also shown a significant upward trend, rising from $1,453 million in 1995 to $72,738 million in 2022, marking an impressive increase of nearly 5,000%. This sustained profitability demonstrates the company's efficient operations and effective cost management strategies.

**Earnings per share (EPS):** MSFT's EPS has followed a generally positive trajectory, reflecting the company's profitability and value creation for shareholders. From $2.32 in 1995, the EPS rose to an all-time high of $9.65 in 2022. This consistent growth in EPS indicates MSFT's ability to generate increasing returns for investors.

**Profitability:** MSFT's gross margin percentage has fluctuated over the years, but it has generally remained within a range of 40% to 47%. This indicates that the company has been successful in maintaining a healthy gross margin, allowing it to cover operating expenses and generate profits.

**Assets:** MSFT's total current assets have witnessed a substantial increase, growing from $5,620 million in 1995 to $169,684 million in 2022. This indicates the company's ability to acquire and manage its assets effectively, providing a strong financial foundation for future growth.

**Liabilities:** MSFT's total current liabilities have also increased over the years, rising from $2,425 million in 1996 to $95,082 million in 2022. This growth in liabilities reflects the company's increasing financial obligations, which need to be carefully managed to maintain a healthy financial position.

**Liquidity:** MSFT's current ratio, which measures the company's ability to meet its short-term obligations, has generally remained above 1.0, indicating that the company has sufficient liquidity to cover its current liabilities. This suggests that MSFT is financially stable and has the resources to meet its immediate financial commitments.

**Summary:**

Overall, the financial performance of MSFT has been remarkable, with consistent growth in revenue, net income, and EPS. The company has demonstrated strong profitability, effective asset management, and a solid financial position. MSFT's ability to adapt to changing market dynamics and maintain a competitive edge has contributed to its long-term success and positions it well for continued growth in the years to come.
~~~

Of course, this output can be made better by giving better prompts to the LLM model, but for now, we can continue with this since we were able to at least extract the relevant information.

## App

I developed a streamlit to showcase insights.

When I launch the app, it opens up like this: you can see that it takes input as a ticker.

<img width="857" alt="Screenshot 2024-05-13 at 3 50 57 PM" src="https://github.com/PulkitDhamija/GeorgiaTechSubmission/assets/82368328/3ba0e09c-4847-403c-97df-af127df2163c">\

You can see that it takes input as a ticker.

<img width="762" alt="Screenshot 2024-05-13 at 3 53 43 PM" src="https://github.com/PulkitDhamija/GeorgiaTechSubmission/assets/82368328/31fc50b1-8b89-4ce4-b644-20160c191cc9">\

After choosing the ticker, the backend code is running to generate the response.

The insights were as follows:



Note: I have only run the app for the past 10 years (2013-2023) as an example. 

## Challenges and Further improvements

- I have only tried to show the generated insights from the LLM model. I did not try to show any visualisations like trend plots for different financial information. We can show that as well by extracting the particular information from LLM outputs and cleaning that if necessary, and finally showcase the trend plots.
- The time it takes to process all the text (chunks and everything) is still really long. I think that can be significantly reduced if we use LLM models, which are specifically made for text summarization. One such LLM model is "text summarize"; it is really fast for the use case of text summarization, and even GPT is better in terms of speed against Gemini. Since Gemini is free to use, I used Gemini for this.

