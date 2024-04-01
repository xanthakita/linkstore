import requests
import re
import pandas as pd
import json

def clean_filename(filename):
    """
    Function to clean up a string to be used as a filename.

    :param filename: The original string to be cleaned up

    :return Cleaned up string safe for use as a filename
    """
    filename = re.sub(r'[\\/*?:"<>|]', "", filename) # remove special characters
    return filename


def build_payload(query, start=1, num=10, date_restrict='m1', **params):
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


def make_request(payload):
    """
    Function to GET a request  to the Google Search API and handle  potential errors.

    :param payload: Dictionary containing the API request parameters
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
        except (ConnectionError, Timeout) as e:
            print(f"Connection error or timeout: {e}")
            retries += 1
    raise Exception('Failed to make request after multiple retries')


def main(query, result_total=10):
    """
    Main function to execute the script.
    """
    items = []
    reminder = result_total % 10
    if reminder > 0:
        pages = (result_total // 10) + 1
    else:
        pages = (result_total // 10)

    for i in range(pages):
        if pages == i + 1 and reminder > 0:
            payload = build_payload(query, start=(i+1)*10, num=reminder)
        else:
            payload = build_payload(query, start=(i+1)*10)
        response = make_request(payload)
        items.extend(response['items'])
    query_string_clean = clean_filename(query)
    
    # Write to JSON file
    with open(f'Google_Search_Result_{query_string_clean}.json', 'w') as json_file:
        json.dump(items, json_file, indent=4)


if __name__ == '__main__':
    API_KEY = 'AIzaSyDe5RN1AKudxHJihyVqolqP5fZlbA3Ui2U'
    SEARCH_ENGINE_ID = 'e05a3190ad1614712'
    search_query=["CSAM", "child protection", "how to identify grooming behaviors", "human-trafficking", "sand-mafias"]
    total_results = 35
    main(search_query, total_results)
