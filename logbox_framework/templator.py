from os.path import join
from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    file_path = join(folder, template_name)

    # Get template by name
    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())
    # Get render and return page
    return template.render(**kwargs)
