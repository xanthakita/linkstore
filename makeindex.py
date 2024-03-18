import os
import json

def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def generate_html_entry(entry):
    html = f"""
    <div class="entry">
        <h2>{entry['title']}</h2>
        <p>{entry['description']}</p>
        <a href="{entry['url']}" target="_blank">Visit Website</a>
    """
    if 'contact-url' in entry:
        html += f"""
        <a href="{entry['contact-url']}" target="_blank">Contact {entry['contact-name']}</a>
        """
    if 'contact-number' in entry:
        html += f"""
        <p>Contact Phone: {entry['contact-number']}</p>
        """
    html += "</div>"
    return html

def generate_html(entries):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Links</title>
    </head>
    <body>
    """
    for entry in entries:
        html += generate_html_entry(entry)
    html += """
    </body>
    </html>
    """
    return html

def main():
    # Get the current working directory
    current_directory = os.getcwd()

    # Initialize an empty list to store all entries
    all_entries = []

    # Iterate through subdirectories
    for subdir, _, files in os.walk(current_directory):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(subdir, file)
                entries = load_json_file(json_file_path)
                all_entries.extend(entries)

    # Generate the HTML content
    html_content = generate_html(all_entries)

    # Write the HTML content to index.html in the root directory
    with open('index.html', 'w') as html_file:
        html_file.write(html_content)

if __name__ == '__main__':
    main()

