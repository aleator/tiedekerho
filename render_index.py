import yaml
from jinja2 import Environment, FileSystemLoader

# Load YAML data
with open("index.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# Set up Jinja2 environment (template assumed to be in the same directory)
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("index.template")

# Render the template with the data
output_html = template.render(data)

# Write the output to an HTML file
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output_html)

print("Index page generated: index.html")
