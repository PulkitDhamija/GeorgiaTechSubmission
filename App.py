import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # to remove unnecessary warning regarding gpu

import streamlit as st

import shutil
from sec_edgar_downloader import Downloader
import re
import google.generativeai as genai

st.title('Georgia Tech Submission')

key = "AIzaSyDv1evgnmqnkRRrcqt1gAlcpJWTgpYKqAo"
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-pro')

@st.cache_data
def filling_downoader(equity):
    dl = Downloader("MyCompanyName", "my.email@domain.com")
    dl.get("10-K", equity, after="2020-12-31", before="2023-12-31", download_details=False)

@st.cache_data
def rename_folder(equity):
    folder_path = "sec-edgar-filings/" + equity + "/10-K"
    pattern = r'-(\d+)-'
    years = []
    for folder_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, folder_name)
        if os.path.isdir(full_path):
            match = re.search(pattern, folder_name)
            if match:
                new_folder_name = match.group(1)
                years.append(new_folder_name)
                new_full_path = os.path.join(folder_path, new_folder_name)
                os.rename(full_path, new_full_path)

    return years

@st.cache_data
def file_paths(equity, years):
    folder_path = "sec-edgar-filings/" + equity + "/10-K"
    file_paths = {}
    for folder_name in years:
        full_path = os.path.join(folder_path, folder_name)
        full_path = full_path + '/'
        if os.path.exists(full_path):
            files = os.listdir(full_path)
            if files:
                file_paths[int(folder_name)] = os.path.join(full_path, files[0])

    return file_paths

@st.cache_data
def first_modification(file_path):

    with open(file_path, 'r') as file:
        lines = file.readlines()
        new_lines = []
        previous_line_has_content = False
        this_is_image = False
        this_is_xlsx = False
        this_is_htm = False
        this_is_zip = False
        for line in lines:
            # Use regular expression to remove content between < and >
            line = re.sub(r'<.*?>', ' ', line)

            if line.strip() == '' and not previous_line_has_content:
                continue
        
            if line.strip() == '&#160;': continue

            if line.strip() == '&nbsp;': continue

            if line.strip() == '&#xA0;': continue

            if line.strip() == '&#160;&#160;': continue

            if line.strip() == '&nbsp;&nbsp;': continue

            if line.strip() == '&#xA0;&#xA0;': continue

            if line.strip() == ' &#150;': continue

            if line.strip() == '':
                previous_line_has_content = False
            else:
                previous_line_has_content = True

            if '.jpg' in line:
                this_is_image = True

            if '.xlsx' in line:
                this_is_xlsx = True

            if '.zip' in line:
                this_is_htm = True

            if '.htm' in line:
                this_is_htm = True


            if line.strip() != '' and this_is_image:
                continue
            else:
                this_is_image = False

            if line.strip() != '' and this_is_xlsx:
                continue
            else:
                this_is_xlsx = False
            
            if line.strip() != '' and this_is_htm:
                continue
            else:
                this_is_htm = False
        
            if line.strip() != '' and this_is_zip:
                continue
            else:
                this_is_zip = False

            
            new_lines.append(line)
             

    write_path = 'modified1.txt'
    with open(write_path, 'w') as file:
            file.writelines(new_lines)

    # print(write_path)
    return write_path

@st.cache_data
def remove_empty_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        new_lines = []
        previous_line_has_content = False
        for line in lines:
            if line.strip() == '' and not previous_line_has_content:
                continue

            if line.strip() == '':
                previous_line_has_content = False
            else:
                previous_line_has_content = True

            new_lines.append(line)

    with open(file_path, 'w') as file:
            file.writelines(new_lines)


@st.cache_data
def second_modification(file_path, max_length=100):
    new_lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        if len(line) > max_length:
            for i in range(0, len(line), max_length):
                new_lines.append(line[i:i+max_length])
        
        else:
            new_lines.append(line)
    
    write_path = "modified2.txt"

    fw = open("modified2.txt", 'w')

    fw.write('\n'.join(new_lines) + '\n')
    
    return write_path


@st.cache_data
def third_modification(file_path):

    keywords = ["Total number of shares purchased",
    "average price paid per share",
    # "Revenue",
    "Total net sales",
    "Total gross margin",
    "Total cost of sale",
    "cost of sale",
    "total gross margin percentage",
    "Net income",
    "Earnings per share ",
    "Total current assets",
    "current assets",
    "Total shareholders’ equity",
    "Total current liabilities",
    "current liabilities",
    "Period end",
    "end period",
    "Total revenue",
    "CURRENT-ASSETS",
    "TOTAL-ASSETS",
    "CURRENT-LIABILITIES",
    "TOTAL-LIABILITY-AND-EQUITY",
    "TOTAL-REVENUES",
    "PERIOD-END",
    "FISCAL-YEAR-END"]
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    
    for i in range(len(lines)):

        keyword_found = False

        for word in keywords:
            if word.lower() in lines[i].lower():
                keyword_found = True
                break

        if keyword_found:

            for j in range(i-2, min(i+8, len(lines))):
                new_lines.append(lines[j])

            i = i+6
    write_path = "modified3.txt"
    with open(write_path, 'w') as file:
        file.writelines(new_lines)
        
    return write_path

@st.cache_data
def fourth_modification(file_path, chunk_size = 500):
    chunks = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    total_lines = len(lines)
    num_chunks = (total_lines + chunk_size - 1) // chunk_size

    for i in range(num_chunks):
        start_index = i * chunk_size
        end_index = min((i + 1) * chunk_size, total_lines)
        chunk = lines[start_index:end_index]
        cont = "".join(chunk)
        chunks.append(cont)

    return chunks


@st.cache_data
def fifth_modification(chunks, max_chunk_size = 8000):
    new_chunks = []
    for chunk in chunks:
        if len(chunk.strip()) > max_chunk_size:
            num_splits = (len(chunk.strip()) + max_chunk_size - 1) // max_chunk_size
            split_size = len(chunk) // num_splits

            for i in range(num_splits):
                start_index = i * split_size
                end_index = min((i + 1) * split_size, len(chunk))
                new_chunk = chunk[start_index:end_index]
                new_chunks.append(new_chunk)
        else:
            new_chunks.append(chunk)

    return new_chunks


@st.cache_data
def response(smaller_chunks, year):
    # print(len(smaller_chunks))
    responses = []
    i = 0
    for chunk in smaller_chunks:
        # print(i)
        i = i+1
            
        prompt = f"""
        extract the information provided below for the {year}
        total number of shares purchased and average price paid per share/number of shares purchases,
        total net sales and year change/net sales, 
        total gross margin and total gross margin percentage/Total cost of sales/gross margin/gross margin percentage, 
        net income/total net income,
        earnings per share,
        total current assets/current assets,
        total shareholders’ equity/shareholders’ equity,
        total current liabilities/current liabilities,
        period end,
        total revenue/revenue."
        The text is as follows: ```{chunk}```
        """

        response = model.generate_content(prompt)
        responses.append(response.text)

    res = "\n".join(responses)
    write_path = "first_response.txt"

    with open(write_path, 'w') as file:
        file.write(res)

    return write_path


@st.cache_data
def removing_unnecessary_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    not_words = [
    'not',
    'Not',
    'No',
    'cannot'
    ]   
    new_lines = []
    
    for i in range(len(lines)):

        keyword_found = False

        for word in not_words:
            if word.lower() in lines[i].lower():
                keyword_found = True
                break

        if keyword_found: continue

        new_lines.append(lines[i])


    write_path = "modified_response.txt"
    with open(write_path, 'w') as file:
        file.writelines(new_lines)
        
    return write_path


@st.cache_data
def final_aggregate_response(path):
    with open(path, 'r') as file:
        res = file.read()

    prompt = f"""
    Aggregate the financial information
    which may include
    "Total number of shares purchased",
    " average price paid per share",
    "Total net sales",
    "Total gross margin",
    "Total cost of sale",
    "cost of sale",
    "total gross margin percentage",
    "Net income",
    "Earnings per share ",
    "Total current assets",
    "current assets"
    "Total shareholders’ equity",
    "Total current liabilities",
    "current liabilities",
    "Period end",
    "end period",
    "Total revenue"
    The info is as follows: ```{res}```
    """

    response = model.generate_content(prompt)
    return response.text


@st.cache_data
def input_fun(years, file_paths):
    all_year_response = {}
    for year in years:
        fillings_path = file_paths[int(year)]
        flag = True
        path = ""
        if year[0] == '9': 
            flag = False
            year = '19' + year
        elif year[0] == '0' and year[1] == '0': 
            flag = False
            year = '20' + year
        else:
            year = '20' + year
        
        if flag:
            path = first_modification(file_path=fillings_path)
            path = second_modification(file_path=path)
        else:
            path = second_modification(file_path=fillings_path)

        remove_empty_lines(file_path=path)
        path = third_modification(file_path=path)
        remove_empty_lines(file_path=path)
        chunks = fourth_modification(file_path=path)
        chunks = fifth_modification(chunks=chunks)
        # print(year, len(chunks))
        path = response(smaller_chunks=chunks, year=year)
        path = removing_unnecessary_info(path)
        res = final_aggregate_response(path)
        all_year_response[int(year)] = res

    return all_year_response


@st.cache_data
def modifying_input(response):
    myKeys = list(response.keys())
    myKeys.sort()
    response = {i: response[i] for i in myKeys}
    input_for_insights = []
    for year, response in response.items():
        input = "FINANCIAL DATA FOR " + str(year) + "\n\n" + response
        input_for_insights.append(input)

    gem_input = "\n\n".join(input_for_insights)

    return gem_input


@st.cache_data
def final_output(gem_input, ticker):
    # ticker = "AAPL"
    final_prompt = f"""
        I am providing you with financial information about the company {ticker} over the years (2021-2023).
        Using this information, generate insights about the performance, also share the numberes wherever necessary,
        be a little extensive, insights which talk about trends and stuff..
        and finally summarize the whole info
        The info is as follows: ```{gem_input}```
        """

    final_response = model.generate_content(final_prompt)
    return final_response.text



ticker = ""
ticker = st.text_input("Ticker:")
st.write("The ticker is: ", ticker)

if ticker != "":
    # model = llm_model()
    filling_downoader(ticker)
    years = rename_folder(ticker)
    paths = file_paths(ticker, years)

    response = input_fun(years=years, file_paths=paths)

    gem_input = modifying_input(response)

    app_out = final_output(gem_input, ticker)

    st.write(app_out)

    folder_path = "sec-edgar-filings"
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)





