import os
import json

def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def generate_html_section(directory, entries):
    def generate_html_entry(entry):
        # Define how each entry should be formatted in HTML
        return f"<p>{entry}</p>"

    html = f"""
    <div class="section">
        <h1>{directory}</h1>
    """
    for entry in entries:
        html += generate_html_entry(entry)
    html += "</div>"
    return html

def generate_html(grouped_entries):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Links</title>
    </head>
    <body>
    """
    for directory, entries in grouped_entries.items():
        html += generate_html_section(directory, entries)
    html += """
    </body>
    </html>
    """
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
        html_file.write(html_content)

if __name__ == '__main__':
    main()

