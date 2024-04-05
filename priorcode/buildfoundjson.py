import requests
from bs4 import BeautifulSoup
import json

# Open the text file and read the URLs
with open('foundlinks.txt', 'r') as f:
    urls = f.read().splitlines()

data = []

for url in urls:
    # Send HTTP request
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title
    title = soup.title.string if soup.title else None

    # Extract the first heading
    heading = soup.h1.string if soup.h1 else None

    # Extract the meta-tags
    meta_tags = {meta.get('name'): meta.get('content') for meta in soup.find_all('meta') if meta.get('name')}

    # Append the data to the list
    data.append({
        'url': url,
        'title': title,
        'heading': heading,
        'meta_tags': meta_tags
    })

# Write the data to a JSON file
with open('foundlinks.json', 'w') as f:
    json.dump(data, f, indent=4)

