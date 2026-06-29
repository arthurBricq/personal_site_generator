"""
A python script that generates your personal website
"""

import argparse
import os
import shutil
from functools import partial

from generator.page_builder import create_index_page
from generator.page_builder import create_page_with_children
from generator.utils import clean_output_dir


def get_header(name, root=".") -> str:
    return f"""
<header>
    {name}
</header>

<nav>
    <a href="{root}/resume.pdf">My resume</a>
    <a href="{root}/writings.html">Writing</a>
    <a href="{root}/projects.html">Projects</a>
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
