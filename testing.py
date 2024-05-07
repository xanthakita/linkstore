# Define the search titles
search_titles = ['CSAM', 'Child Protection', 'Sand Mafia']

# Define the corresponding rules for each search title
search_rules = {
    'FILES': "(filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xls OR filetype:xlsx OR filetype:ppt OR filetype:pptx OR filetype:csv OR filetype:txt OR filetype:json)",
    'NEWS': "inurl:NEWS (filetype:htm OR filetype:html)",
    'WEB': "(filetype:htm OR filetype:html)"
}

# Define the search modifiers for each search title
search_modifiers = {
    'CSAM': "inurl:CSAM -inurl:'Customer Success Account Manager'",
    'Child Protection': "intitle:'Child Protection'",
    'Sand Mafia': "intitle:'Sand Mafia'"
}

# Initialize an empty list to store the search strings
search_strings = []

# Generate search strings based on the search titles, modifiers, and rules
for title in search_titles:
    for modifier_title, modifier in search_modifiers.items():
        if modifier_title in title:
            for rule_title, rule in search_rules.items():
                search_strings.append([f"{title} {rule_title}", modifier, f"{modifier} {rule}"])
            break

# Print the generated search strings
for search_string in search_strings:
    print(search_string)
