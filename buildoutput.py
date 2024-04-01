import os
import json


def extract_info(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract required information
    info = {
        "title": data.get("title", ""),
        "link": data.get("link", ""),
        "displayLink": data.get("displayLink", ""),
        "snippet": data.get("snippet", ""),
        "formattedUrl": data.get("formattedUrl", ""),
    }
    
    # Check if metatags is a list and extract its elements
    metatags = data.get("pagemap", {}).get("metatags", [])
    if isinstance(metatags, list) and len(metatags) > 0:
        info["metatags"] = metatags[0]  # Only take the first element if it's a list
    else:
        info["metatags"] = {}
    
    return info

def write_info(info, output_file):
    with open(output_file, 'w') as f:
        json.dump(info, f, indent=4)

def process_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_file = os.path.join(root, file)
                info = extract_info(json_file)
                output_file = f"linkstore_{file}"
                write_info(info, output_file)

if __name__ == "__main__":
    process_files(".")

