"""
A python script that generates your personal website
"""

import argparse
import os
import shutil
from functools import partial

from generator.page_builder import create_index_page
from generator.page_builder import create_page_with_children
from generator.page_builder import GITHUB_ICON
from generator.utils import clean_output_dir

GITHUB_URL = "https://github.com/arthurBricq"
LINKEDIN_URL = "https://www.linkedin.com/in/arthur-bricq-737548153/"

LINKEDIN_ICON = (
    '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="currentColor" aria-hidden="true">'
    '<path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56'
    'h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 110-4.13 2.06 2.06 0 '
    '010 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 '
    '0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>'
)


def get_header(name, root=".") -> str:
    return f"""
<header>
    <span class="site_name">{name}</span>
    <a class="social" href="{GITHUB_URL}" aria-label="GitHub">{GITHUB_ICON}</a>
    <a class="social" href="{LINKEDIN_URL}" aria-label="LinkedIn">{LINKEDIN_ICON}</a>
</header>

<nav>
    <a href="{root}/resume.pdf">Resume</a>
    <a href="{root}/projects.html">Portfolio</a>
    <a href="{root}/writings.html">Writing</a>
    <a href="{root}/index.html">About</a>
</nav>
    """


def main():
    parser = argparse.ArgumentParser(description="Generate the personal website.")
    parser.add_argument("--data", default="./data", help="Content source directory")
    parser.add_argument("--templates", default="./templates", help="Templates directory")
    parser.add_argument("--output", default="./outsite", help="Output directory")
    parser.add_argument("--name", default="Arthur Bricq", help="Site owner name (shown in the header)")
    args = parser.parse_args()

    print("Starting to generate site")

    header_getter = partial(get_header, args.name)

    # clean build: wipe the output (preserving .git and CNAME of the hosting repo)
    clean_output_dir(args.output)

    # create project page
    create_page_with_children(
        site_root=args.output,
        page_name="projects",
        page_template=os.path.join(args.templates, "projects.html"),
        children_template=os.path.join(args.templates, "children_template.html"),
        page_container_id="projects_list",
        children_input_path=os.path.join(args.data, "projects"),
        header_getter=header_getter
    )
    print("Projects generated successfully")

    # create writing page
    create_page_with_children(
        site_root=args.output,
        page_name="writings",
        page_template=os.path.join(args.templates, "writing.html"),
        children_template=os.path.join(args.templates, "children_template.html"),
        page_container_id="article_list",
        children_input_path=os.path.join(args.data, "writing"),
        header_getter=header_getter
    )
    print("Articles generated successfully")

    # create main page
    create_index_page(
        template_path=os.path.join(args.templates, "index.html"),
        content_path=os.path.join(args.data, "main_page.md"),
        output_path=os.path.join(args.output, "index.html"),
        container_id="markdown_container",
        header_getter=header_getter)
    print("Main page generated successfully")

    # cp images into output
    shutil.copytree(os.path.join(args.data, "images"), os.path.join(args.output, "images"), dirs_exist_ok=True)

    # cp style and resume
    shutil.copyfile(os.path.join(args.templates, "style.css"), os.path.join(args.output, "style.css"))
    shutil.copyfile(os.path.join(args.data, "resume.pdf"), os.path.join(args.output, "resume.pdf"))

    print("ressources copied successfully")
    print("finished")


if __name__ == "__main__":
    main()
