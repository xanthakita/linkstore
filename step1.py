import os
import requests
import re
import json
import ollama
import pandas as pd
from dotenv import load_dotenv, dotenv_values
import time
import random

# from google_api import API_KEY, SEARCH_ENGINE_ID

load_dotenv()

API_KEY = os.environ.get("API_KEY")
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")

def load_ollama_model():
    # Load or initialize the Ollama model here
    # Example: return ollama.load_model('llava')
    return {'model': 'llava', 'created_at': '2024-04-25T11:49:50.180199Z', 'message': {'role': 'assistant', 'content': ''}, 'done': True}

def clean_summary(summary):
    # Remove any non-text characters from the summary
    cleaned_summary = re.sub(r'\W+', ' ', summary)
    return cleaned_summary.strip()

def ollamareq(links):
      
    summaries = []
    for link in links:
        response = ollama.generate(model='llava:latest', prompt=f"Please summarize the content of the link {link}")
        if 'response' in response:
            summaries.append(response['response'])
        else:
            print("Failed to retrieve summary from Ollama.")
            return None
        
    print(f"Summaries: {summaries}")
    return summaries


# def ollamareq(ollama_model, links):
#    # Use the Ollama model to make requests
#    response = ollama.chat(model=ollama_model['model'], chat_messages=[{'role': 'user', 'content': link} for link in links])
#    return response['message']['content']

#def ollamareq(ollama_model, links):
#    model_name = ollama_model['model']
#    response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': f"Please summarize the link: {link} and return the summary as ollama_summary in a json object." } for link in links])
#    # print(f"returned:{response['message']['content']}")
#    return response['message']['content']


def clean_filename(filename: str) -> str:
    """
    Function to clean up a string to be used as a filename.

    :param filename: The original string to be cleaned up

    :return Cleaned up string safe for use as a filename
    """
    filename = re.sub(r'[\\/*?:"<>|]', "", filename) # remove special characters
    return filename

def build_payload(query: str , start=1, num=10, date_restrict='m1', **params) -> dict :
    """
    function to build the payload for the Google search API request.

    :param query: Search term
    :param start: The index of the first result to return
    :param link_site: Specifies that all search results should contain a link to a particular url
    :param search_type: Type of Search (default is undefined, 'IMAGE' for image search)
    :param date_restrict: Restricts results based on recency (default is 1 month 'm1')
    :param params: Additional parameters for the API request

    :return: Dictionary containing the API request parameters
    """
    payload = {
            'key': API_KEY,
            'q': query,
            'cx': SEARCH_ENGINE_ID,
            'start': start,
            'num': num,
            'language': 'en',
            'dateRestrict': date_restrict
    }

    payload.update(params)
    
    # print(payload)
    return payload

def make_request(payload: dict, max_retries=3) -> str :
    """
    Function to GET a request  to the Google Search API and handle  potential errors.

    :param payload: Dictionary containing the API request parameters
    :param max_retries: Maximum number of retries for the request
    :return: JSON response from the API
    """
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get('https://www.googleapis.com/customsearch/v1', params=payload)
            if response.status_code == 200:
                return response.json()  # Return JSON response
            else:
                print(f"Request failed with status code: {response.status_code}")
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Connection error or timeout: {e}")
            retries += 1
    raise Exception('Failed to make request after multiple retries')

def check_existing_links(links: list, existing_files: list) -> str :
    existing_links = []
    for file in existing_files:
        with open(file, 'r') as f:
            data = json.load(f)
            existing_links.extend([item['link'] for item in data])
    return [link for link in links if link not in existing_links]

def main(filename, query, result_total=10):
    """
    Main function to execute the script.
    """
    ollama_model = load_ollama_model()
    # print(f"Current Search Query: {query}")
    # print(f"Output Filename: Google_Search_Result_{clean_filename(filename)}.json")
    items = []
    reminder = result_total % 10
    if reminder > 0:
        pages = (result_total // 10) + 1
    else:
        pages = (result_total // 10)

    for i in range(pages):
        current_start = i * 10 + 1
        if pages == i + 1 and reminder > 0:
            current_num = reminder
        else:
            current_num = 10
                
        payload = build_payload(query, start=current_start, num=current_num)
        # print(f"Current Payload: {payload}")
        response = make_request(payload)
        if 'items' in response:
            items.extend(response['items'])

    query_string_clean = clean_filename(filename)

    existing_files = [file for file in os.listdir() if file.startswith("Google_Search_Result_") and file.endswith(".json")]
    new_links = check_existing_links([item['link'] for item in items], existing_files)
    new_items = [item for item in items if item['link'] in new_links]

    # Get summaries for new items
    links = [item['link'] for item in new_items]
    summaries = ollamareq(links)
    # print(f"model: {ollama_model}")
    # print(f"links: {links}")
    # print(f"summaries: {summaries}")

    # Attach summaries to new items
 #   for i, item in enumerate(new_items):
 #      item['summary'] = summaries[i]

    # Attach summaries to new items
    for i, item in enumerate(new_items):
        if i < len(summaries):
            item['ollama_summary'] = summaries[i]
        else:
            print(f"No summary available for item {i}")

    # Debugging statements
    print("Type of summaries:", type(summaries))
    print("Length of summaries:", len(summaries))


    # Write to JSON file with the updated file name
    with open(f'Google_Search_Result_{query_string_clean}.json', 'w') as json_file:
        json.dump(new_items, json_file, indent=4)

if __name__ == '__main__':
    search_queries = [
        ["CSAM_FILES", "CSAM -Manager -Management -Mathematics -hiring filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xls OR filetype:xlsx OR filetype:ppt OR filetype:pptx"], 
        #["CSAM PDF", "intitle:'CSAM' -'Customer Success Account Management' -'Manager' -'hiring' filetype:pdf"], 
        ["CSAM_HTML", "CSAM -Manager -Management -Mathematics -hiring -filetype:pdf AND -filetype:doc AND -filetype:docx AND -filetype:xls AND -filetype:xlsx AND -filetype:ppt AND -filetype:pptx"], 
        #["CSAM CSV", "intitle:'CSAM' -'Customer Success Account Management' -'Manager' -'hiring' -filetype:csv"],
        #["CSAM TXT", "inalltext:'CSAM' -'Customer Success Account Management' -'Manager' -'hiring' -filetype:txt"],
        ["Child_Protection_FILES","child protection (filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xls OR filetype:xlsx OR filetype:ppt OR filetype:pptx OR filetype:csv OR filetype:txt OR filetype:json)"],
        #["Child Protection PDF", "intitle:'child protection' filetype:pdf"],   
        ["Child_Protection_HTML", "child protection (-filetype:pdf AND -filetype:doc AND -filetype:docx AND -filetype:xls AND -filetype:xlsx AND -filetype:ppt AND -filetype:pptx"], 
        #["Child Protection TXT", "intitle:'child protection' -filetype:txt"], 
        ["Massage_Parlors_and_Trafficking_FILES", "'massage parlors' AND Trafficking -filetype:pdf AND -filetype:doc AND -filetype:docx AND -filetype:xls AND -filetype:xlsx AND -filetype:ppt AND -filetype:pptx"], 
        #["Massage Parlors & Trafficking PDF", "intitle:'massage parlors' & 'trafficking' filetype:pdf"], 
        ["Massage_Parlors_and_Trafficking_HTML", "'massage parlors' AND Trafficking -filetype:pdf AND -filetype:doc AND -filetype:docx AND -filetype:xls AND -filetype:xlsx AND -filetype:ppt AND -filetype:pptx"], 
        #["Massage Parlors & Trafficking TXT", "intitle:'massage parlors' & 'trafficking' -filetype:txt"], 
        ["Trafficking_FILES", "intitle:'trafficking' filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xls OR filetype:xlsx OR filetype:ppt OR filetype:pptx"], 
        #["Trafficking PDF", "intitle:'trafficking' filetype:pdf"], 
        ["Trafficking_HTML", "intitle:'trafficking' -filetype:pdf AND -filetype:doc AND -filetype:docx AND -filetype:xls AND -filetype:xlsx AND -filetype:ppt AND -filetype:pptx"], 
        #["Trafficking TXT", "intitle:'trafficking' -filetype:txt"], 
        ["Sand_Mafia_FILES", "intitle:'sand mafia' filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xls OR filetype:xlsx OR filetype:ppt OR filetype:pptx"], 
        #["Sand Mafia PDF", "intitle:'sand mafia' filetype:pdf"],
        #["Sand Mafia TXT", "intitle:'sand mafia' filetype:txt"],
        ["Sand_Mafia_HTML", "intitle:'sand mafia' -filetype:pdf AND -filetype:doc AND -filetype:docx AND -filetype:xls AND -filetype:xlsx AND -filetype:ppt AND -filetype:pptx"], 
        ["GEN_Links","link:'globalemancipation.ngo'"],
        ["GEN_Related","related:'globalemancipation.ngo'"]
        
    ]
    total_results = 75
    for query_info in search_queries:
        # print(query_info)
        main(*query_info, total_results)
        # Introduce a random delay between 15 to 45 seconds
        delay = random.randint(10, 15)
        print(f"Waiting for {delay} seconds before next search...")
        time.sleep(delay)
