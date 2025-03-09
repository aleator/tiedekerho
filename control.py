import argparse
import os
import re
import yaml
from datetime import datetime

def slugify(name):
    # Lowercase, replace spaces with underscores, remove non-alphanumeric characters.
    slug = name.lower()
    slug = re.sub(r'\s+', '_', slug)
    slug = re.sub(r'[^\w\-]', '', slug)
    return slug

def main():
    parser = argparse.ArgumentParser(
        description="Update index.yaml: move current event(s) to past, add a new event, and create its YAML template."
    )
    parser.add_argument("name", help="Name of the new event")
    parser.add_argument("--date", default="TBD", help="Event date (default: TBD)")
    args = parser.parse_args()

    event_name = args.name
    event_date = args.date

    index_file = "index.yaml"
    # Load existing index.yaml
    with open(index_file, "r", encoding="utf-8") as f:
        index_data = yaml.safe_load(f)

    # Move all upcoming events to past_events, placing the latest moved event at the top.
    upcoming = index_data.get("upcoming_events", [])
    past = index_data.get("past_events", [])
    if upcoming:
        # Prepend upcoming events to past events
        index_data["past_events"] = upcoming + past
        index_data["upcoming_events"] = []

    # Generate file names using a slugified event name
    slug = slugify(event_name)
    new_html_filename = f"toimintailmoitus-{slug}.html"
    new_yaml_filename = f"toimintailmoitus-{slug}.yaml"

    # Create new event entry
    new_event_entry = {
        "href": new_html_filename,
        "event_name": event_name,
        "event_date": event_date
    }
    index_data.setdefault("upcoming_events", []).append(new_event_entry)

    # Save updated index.yaml
    with open(index_file, "w", encoding="utf-8") as f:
        yaml.dump(index_data, f, allow_unicode=True, sort_keys=False)

    # Create a new YAML template for the new event with default sections
    today = datetime.today().strftime("%d.%m.%Y")
    new_event_data = {
        "title": event_name,
        "back_link": "index.html",
        "page_heading": event_name,
        "subheading": "",
        "sections": [
            {
                "title": "Kerhossa tapahtuu:",
                "content": (
                    "Loremipsum"
                )
            },
            {
                "title": "Tarvittavat materiaalit:",
                "content": (
                    "loremipsum"
                ),
                "list": [
                    "A",
                    "B"
                ]
            },
            {
                "title": "Riskit ja turvasuunnitelma:",
                "content": (
                    "Lorem ipsum"
                )
            },
        ],
        "gallery": [],
        "footer": f"Kintauden pientiedekerho | {today}"
    }
    
    with open(new_yaml_filename, "w", encoding="utf-8") as f:
        yaml.dump(new_event_data, f, allow_unicode=True, sort_keys=False)

    print(f"Updated {index_file}: moved current events to past (latest on top) and added new event '{event_name}'.")
    print(f"Created new event YAML file: {new_yaml_filename}")
    print(f"New event HTML will be generated as: {new_html_filename}")

if __name__ == "__main__":
    main()
