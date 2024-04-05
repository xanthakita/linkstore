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
    # Generate card for each entry

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Links</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            /* Custom CSS for additional styling */
            .section {
                background-color: #f8f9fa; /* Light gray background for sections */
                margin-bottom: 20px;
            }
            .card-header {
                cursor: pointer; /* Set cursor to pointer for card headers */
            }
        </style>
    </head>
    <body>
    """

    # Iterate over grouped entries
    for category, entries in grouped_entries.items():
        # Check if category starts with "Google_Search_Result_"
        if category.startswith("Google_Search_Result_"):
            # Format category name without underscores
            category_display = category.replace('_', ' ').replace('Google Search Result ', '').title()

            # Generate card section for each category
            html += f"""
            <div class="container">
                <div class="card section mb-3">
                    <div class="card-header">
                        <h5 class="mb-0">{category_display}</h5>
                    </div>
                    <div class="card-body">
            """

            # Iterate over entries in the category
            for entry in entries:
                title = entry.get('title', 'No Data Available')
                link = entry.get('link', '#')
                display_link = entry.get('displayLink', '')
                formatted_url = entry.get('formattedUrl', '')
                snippet = entry.get('snippet', '')  # Fetch snippet from JSON data

                # Generate card for each entry
                html += f"""
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title"><a href="{link}">{title}</a></h5>
                            <p class="card-text">{snippet}</p>
                            <p class="card-text">{display_link}</p>
                            <p class="card-text">{formatted_url}</p>
                        </div>
                    </div>
                """

            # Close card body and section
            html += """
                    </div>
                </div>
            </div>
            """

    # Include Bootstrap 4 JavaScript files
    html += """
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
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
                # Extract source file name without extension
                sourcefile = os.path.splitext(file)[0]
                grouped_entries[sourcefile] = entries

    # Generate the HTML content
    html_content = generate_html(grouped_entries)

    # Write the HTML content to index.html in the root directory
    with open('index.html', 'w') as html_file:
        # Write the HTML content
        html_file.write(html_content)

        # Include Bootstrap 4 JavaScript files for collapse functionality
        html_file.write("""
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        """)

if __name__ == '__main__':
    main()


