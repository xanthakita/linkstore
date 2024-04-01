import os
import requests

# Replace 'YOUR_API_KEY' and 'YOUR_CX' with your actual API key and Custom Search Engine ID
API_KEY = 'AIzaSyBbNhF4x6qxbEUHWqEqmuNtfw9L4414C7E'
CX = 'e05a3190ad1614712'

def google_search(query):
    """Searches Google for the given query and returns the results."""
    # url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}"
    url = f"GET https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Return JSON response
    else:
        # Handle errors
        print("Error: Failed to retrieve search results.")
        return None

if __name__ == "__main__":
    topics = ["CSAM", "child protection", "how to identify grooming behaviors", "human-trafficking", "sand-mafias"]

    for topic in topics:
        print(f"Searching for: {topic}")

        # Create subdirectory for each topic
        topic_dir = topic.replace(' ', '_')
        os.makedirs(topic_dir, exist_ok=True)

        # Google search
        query = topic
        search_results = google_search(query)

        if search_results and 'items' in search_results:
            # Extract and dump links to file
            filename = os.path.join(topic_dir, "links.txt")
            with open(filename, "w") as f:
                for item in search_results['items']:
                    link = item.get('link')
                    if link:
                        f.write(link + "\n")
                print(f"Links dumped to {filename}\n")
        else:
            print("No results found.\n")

