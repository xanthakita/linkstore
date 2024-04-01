import requests
from bs4 import BeautifulSoup

topics = ["CSAM", "child protection", "how to identify grooming behaviors", "human-trafficking", "sand-mafias"]

def searx_search(query):
  """Searches SearxNG for the given query and returns the results."""

  url = "http://localhost:8080/search?q={}".format(query)
  response = requests.get(url)
  #results = response.json()
  # Check if the response is successful
  if response.status_code == 200:
      return response.json()  # Parse JSON response
  else:
      # Handle errors
      print("Error: Failed to retrieve search results.")
      return None

if __name__ == "__main__":

    for topic in topics:
        print(f"Searching for: {topic}")
    
        # Google search URL
        query = f"{topic.replace(' ', '+')}"
        response = searx_search(query)    
        # Send HTTP request
        # response = requests.get(url)
    
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
    
        # Find all search result links
        links = soup.find_all('a')
    
        for link in links:
            url = link.get('href')
        
            # Filter out unnecessary links
            if url.startswith("/url?q="):
                print(url[7:])
        print("\n")
