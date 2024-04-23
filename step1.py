import os
import requests
import re
import json
import pandas as pd
from dotenv import load_dotenv, dotenv_values
import time
import random

# from google_api import API_KEY, SEARCH_ENGINE_ID

load_dotenv()

API_KEY = os.environ.get("API_KEY")
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")

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
            'dateRestrict': date_restrict
    }

    payload.update(params)
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
    print(f"Current Search Query: {query}")
    print(f"Output Filename: Google_Search_Result_{clean_filename(filename)}.json")
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
        print(f"Current Payload: {payload}")
        response = make_request(payload)
        if 'items' in response:
            items.extend(response['items'])

    query_string_clean = clean_filename(filename)

    existing_files = [file for file in os.listdir() if file.startswith("Google_Search_Result_") and file.endswith(".json")]
    new_links = check_existing_links([item['link'] for item in items], existing_files)
    new_items = [item for item in items if item['link'] in new_links]

    # Write to JSON file with the updated file name
    with open(f'Google_Search_Result_{query_string_clean}.json', 'w') as json_file:
        json.dump(new_items, json_file, indent=4)

if __name__ == '__main__':
    search_queries = [
        ["CSAM PDF", "intitle:'CSAM' -'Customer Success Account Management' -'hiring' filetype:pdf"], 
        ["Child Protection PDF", "intitle:'child protection' filetype:pdf"], 
        ["Massage Parlors & Trafficking PDF", "intitle:'massage parlors' & 'trafficking' filetype:pdf"], 
        ["Trafficking PDF", "intitle:'trafficking' filetype:pdf"], 
        ["Sand Mafia PDF", "intitle:'sand mafia' filetype:pdf"],
        ["CSAM HTML", "intitle:'CSAM' -'Customer Success Account Management' -'hiring' -filetype:html"], 
        ["Child Protection HTML", "intitle:'child protection' -filetype:html"], 
        ["Massage Parlors & Trafficking HTML", "intitle:'massage parlors' & 'trafficking' -filetype:html"], 
        ["Trafficking HTML", "intitle:'trafficking' -filetype:html"], 
        ["Sand Mafia HTML", "intitle:'sand mafia' -filetype:html"],
        ["CSAM CSV", "intitle:'CSAM' -'Customer Success Account Management' -'hiring' -filetype:csv"]
    ]
    total_results = 75
    for query_info in search_queries:
        print(query_info)
        main(*query_info, total_results)
        # Introduce a random delay between 15 to 45 seconds
        delay = random.randint(3, 7)
        print(f"Waiting for {delay} seconds before next search...")
        time.sleep(delay)
