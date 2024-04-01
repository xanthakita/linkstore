import os
import json

def extract_info(json_file):
    with open(json_file, 'r') as f:
        data_list = json.load(f)
    
    # Initialize a list to store information from each dictionary
    info_list = []

    # Iterate over each dictionary in the list
    for data in data_list:
        # Extract required information from each dictionary
        info = {
            "title": data.get("title", ""),
            "link": data.get("link", ""),
            "displayLink": data.get("displayLink", ""),
            "snippet": data.get("snippet", ""),
            "formattedUrl": data.get("formattedUrl", ""),
        }
        
        # Check if metatags exist and extract them
        pagemap = data.get("pagemap", {})
        if "metatags" in pagemap:
            info["metatags"] = pagemap["metatags"][0] if pagemap["metatags"] else {}
        else:
            info["metatags"] = {}

        # Append the extracted information to the list
        info_list.append(info)

    return info_list

def process_files(directory):
    for filename in os.listdir(directory):
        if filename.startswith("Google_Search_Result_") and filename.endswith(".json"):
            json_file = os.path.join(directory, filename)
            info_list = extract_info(json_file)
            output_filename = f"linkstore_{filename[23:-5]}.json"  # Extracting the type from filename
            with open(output_filename, 'w') as outfile:
                json.dump(info_list, outfile, indent=4)

if __name__ == "__main__":
    process_files(".")

