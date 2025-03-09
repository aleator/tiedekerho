import yaml
from jinja2 import Environment, FileSystemLoader
import sys

# Load the YAML data
with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# Setup Jinja2 environment (assumes the template is in the same directory)
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("toimintailmoitus.template")

# Render the template with the data from YAML
output_html = template.render(data)

print(output_html)
