import requests
import ollama

def get_ollama_summary(url):

    response = ollama.generate(model='llava:latest', prompt=f"Please summarize the content of the link {url}")
    if 'response' in response:
        return response['response']
    else:
        print("Failed to retrieve summary from Ollama.")
        return None


if __name__ == "__main__":
    # Example usage
    url = input("Enter URL: ")
    summary = get_ollama_summary(url)
    if summary:
        print("Summary:")
        print(summary)
    else:
        print("Failed to retrieve summary from Ollama.")
