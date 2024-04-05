import os
import json

def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        try:
            return json.load(json_file)
        except json.JSONDecodeError as e:
            # Print the file path and the line where the error occurred
            print(f"Error decoding JSON in file: {file_path}")
            print("Error message:", e)
            json_file.seek(0)  # Reset file pointer
            lines = json_file.readlines()
            print("File content:")
            for i, line in enumerate(lines, start=1):
                print(f"Line {i}: {line.strip()}")
            raise  # Re-raise the exception

def generate_html(grouped_entries):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Links</title>
        <style>
            .tag-radio {
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
    """

    # Collect all unique tag values
    all_tags = set()
    for entries in grouped_entries.values():
        for entry in entries:
            for tag_value in entry['tags'].values():
                all_tags.add(tag_value)

    # Generate radio buttons for each unique tag value
    html += "<div class='tag-radio'><form>"
    for tag_value in all_tags:
        html += f"""
        <label><input type="checkbox" name="{tag_value}" value="{tag_value}" checked>{tag_value}</label><br>
        """
    html += "</form></div>"

    # Generate HTML sections for each directory
    for directory, entries in grouped_entries.items():
        html += generate_html_section(directory, entries)

    html += """
    </body>
    </html>
    """
    return html

def generate_html_section(directory, entries):
    # Extracting the last word of the directory path
    directory_name = directory.split('/')[-1]

    html = f"""
    <div class="section {directory_name.lower()}">
        <h1>{directory_name}</h1>
    """

    # Displaying entries with their details
    for entry in entries:
        # Check if each attribute exists and is not empty
        title = entry.get('title', 'No Data Available')
        url = entry.get('url', '#')
        description = entry.get('description', 'No Data Available')
        contact_name = entry.get('contact-name', 'No Data Available')
        contact_url = entry.get('contact-url', '#')
        contact_number = entry.get('contact-number', 'No Data Available')

        html += f"""
        <div class="entry">
            <a href="{url}">{title}</a> - {description}<br>
            Contact: <a href="mailto:{contact_url}">{contact_name}</a> ({contact_number})<br>
            Tags:
        """
        for tag_category, tag_value in entry.get('tags', {}).items():
            html += f"<span class='tag'>{tag_category}: {tag_value}</span>"
        html += "</div>"

    html += "</div>"
    return html


def main():
    # Get the current working directory
    current_directory = os.getcwd()

    # Initialize an empty dictionary to store grouped entries
    grouped_entries = {}

    # Iterate through subdirectories
    for subdir, _, files in os.walk(current_directory):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(subdir, file)
                entries = load_json_file(json_file_path)
                grouped_entries[subdir] = entries

    # Generate the HTML content
    html_content = generate_html(grouped_entries)

    # Write the HTML content to index.html in the root directory
    with open('index.html', 'w') as html_file:
        # Write the HTML content
        html_file.write(html_content)

        # Include filter.js
        html_file.write('<script src="filter.js"></script>')


if __name__ == '__main__':
    main()

