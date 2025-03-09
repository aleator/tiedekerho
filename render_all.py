import os
import yaml
from jinja2 import Environment, FileSystemLoader

# Load the index.yaml file containing event links
with open("index.yaml", "r", encoding="utf-8") as f:
    index_data = yaml.safe_load(f)

# Set up the Jinja2 environment assuming templates are in the current directory.
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("toimintailmoitus.template")

# Collect all event links from upcoming and past events
event_links = []
for event_list in ["upcoming_events", "past_events"]:
    for event in index_data.get(event_list, []):
        event_links.append(event['href'])

# Optionally, remove duplicates
event_links = list(dict.fromkeys(event_links))

# Process each link: swap .html with .yaml and render the page.
for link in event_links:
    data_file = os.path.splitext(link)[0] + ".yaml"
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            page_data = yaml.safe_load(f)
        
        rendered_html = template.render(page_data)
        
        # Save rendered HTML using the original .html link name.
        with open(link, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        
        print(f"Rendered {link} from {data_file}")
    except FileNotFoundError:
        print(f"Warning: {data_file} not found. Skipping {link}.")
