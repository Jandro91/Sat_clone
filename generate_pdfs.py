import csv
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("certificate_template.html")

# Создание папки, если нет
os.makedirs("certificates", exist_ok=True)

with open("users.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        output_path = os.path.join("certificates", row["pdf_file"])
        rendered_html = template.render(login=row["login"])
        HTML(string=rendered_html, base_url=".").write_pdf(output_path)
        print(f"✔ Created PDF: {output_path}")
