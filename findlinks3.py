import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

topics = ["CSAM", "child protection", "how to identify grooming behaviors", "human-trafficking", "sand-mafias"]

def searx_search(query):
    """Searches SearxNG for the given query and returns the results."""
    # url = "http://localhost:8080/search?q={}".format(query)    
    url = "https://google.com/search?q={}".format(query)
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # Return HTML content
    else:
        # Handle errors
        print("Error: Failed to retrieve search results.")
        return None

if __name__ == "__main__":
    for topic in topics:
        print(f"Searching for: {topic}")

        # Create subdirectory for each topic
        topic_dir = topic.replace(' ', '_')
        os.makedirs(topic_dir, exist_ok=True)

        # Google search URL
        query = f"{topic.replace(' ', '+')}"
        html_content = searx_search(query)

        if html_content:
            # Parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all search result links
            links = soup.find_all('a', href=True)

            # Create a file to dump links for the topic
            filename = os.path.join(topic_dir, "links.txt")
            with open(filename, "w") as f:
                for link in links:
                    url = link['href']

                    # Extract and decode the URL
                    url = unquote(url.split('url=')[1])

                    # Write the decoded URL to the file
                    f.write(url + "\n")
                print(f"Links dumped to {filename}\n")
        else:
            print("No results found.\n")



