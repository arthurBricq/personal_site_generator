import bs4
import markdown2
from datetime import datetime
from pathlib import Path

from .utils import clear_folder


def _process_children_page_title(meta):
    return meta["title"].replace(" ", "-")


def _format_month_year(iso):
    return datetime.strptime(iso.strip(), "%Y-%m-%d").strftime("%b %Y")


def _format_dates(meta):
    """Return a display string for a child's date(s), or None if absent.

    Projects use start_date/end_date (collapsed when equal); writings use date.
    Any of these may be omitted, in which case nothing is shown.
    """
    start, end = meta.get("start_date"), meta.get("end_date")
    if start or end:
        start_s = _format_month_year(start) if start else None
        end_s = _format_month_year(end) if end else None
        if start_s and end_s:
            return start_s if start_s == end_s else f"{start_s} – {end_s}"
        return start_s or end_s
    if meta.get("date"):
        return _format_month_year(meta["date"])
    return None


class PageBuilder:
    """
    A class to build an html page and all its related children pages.
    """

    def __init__(self, site_root, page_name, html_editor, template, header_getter):
        """
        Inputs
        ------
        * html_editor: where to put the list of description and links towards the children page
        * template: template for the children page
        * children_output_path: where to write the generated pages
        * header_getter: functions that returns the "header" as a function of the "root"
        """
        self._root = site_root
        self._name = page_name
        self._editor = html_editor
        self._template_path = template
        self._header = header_getter
        clear_folder(site_root + page_name)

    def add_children(self, meta, soup):
        """
        Add a project to the page's content
        * meta contains information about the project
        * soup contains the parsed
        """
        # create html div with a link to the project's page.
        tag = self.add_html_link_to_parent_page(meta)

        # Modify the project page
        self._editor.append(tag)

        # Create a new page with the project's description
        self._create_project_page(meta, soup)

    def _create_project_page(self, _meta, _soup):
        # Load the template for children pages
        with Path(self._template_path).open() as data:
            html_text = data.read()
        if html_text is None:
            print("ERROR opening project's page html template")

        # Find where to add information
        template = bs4.BeautifulSoup(html_text, "html.parser")
        box = template.find(id="content")
        if box is None: return

        # Fill the template with the provided html
        box.append(_soup)

        # Fill the header
        header_container = template.find(id = "header_container")
        if header_container is None: return
        parsed = bs4.BeautifulSoup(self._header(root = ".."), "html.parser")
        header_container.append(parsed)

        # Save the file
        title = _process_children_page_title(_meta)
        with open(self._root + self._name + f"/{title}.html", "w") as file:
            file.write(str(template))

    def add_html_link_to_parent_page(self, _meta):
        children_path = _process_children_page_title(_meta)
        title = _process_children_page_title(_meta)
        html_list = ""
        html_list += (
            '<li class="project_item"><a href="./{}/{}.html">{}</a> </li>'.format(
                self._name, title, _meta["title"]
            )
        )
        dates = _format_dates(_meta)
        if dates:
            html_list += '<p class="date">{}</p>'.format(dates)
        if "keywords" in _meta:
            html_list += '<p class="keyword">{}</p>'.format(_meta["keywords"])
        if "github" in _meta:
            html_list += (
                '<p class="description">Link to <a href="{}">Github</a></p>'.format(
                    _meta["github"]
                )
            )

        # Add the description
        html_list += '<p class="description">{}</p>'.format(_meta["description"])
        # Add the image
        if "featuredImage" in _meta:
            html_list += '<img src="{}" class="thumbnail">'.format(_meta["featuredImage"])

        tag = bs4.BeautifulSoup(html_list, "html.parser")
        return tag


def create_index_page(
    template_path, content_path, output_path, container_id, header_getter
):
    """
    Creates the index.html page by filling the template path from the content found in .md file
    """
    # read the template
    with Path(template_path).open() as data:
        html_text = data.read()
    if html_text is None:
        print("ERROR opening project html")

    # create container with the html elements
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    text_container = soup.find(id=container_id)
    if text_container is None: return

    # read the content
    with Path(content_path).open() as data:
        content = data.read()
    if content is None:
        print("ERROR opening project html")

    # parse and add the markdown
    html = markdown2.markdown(content)
    parsed = bs4.BeautifulSoup(html, "html.parser")
    text_container.append(parsed)

    # fill the header
    header_container = soup.find(id = "header_container")
    if header_container is None: return
    parsed = bs4.BeautifulSoup(header_getter(), "html.parser")
    header_container.append(parsed)

    # save the output
    with open(output_path, "w") as file:
        file.write(str(soup))


def create_page_with_children(
    site_root,
    page_name,
    page_template,
    children_template,
    page_container_id,
    children_input_path,
    header_getter
):
    """
    Creates a page with associated children pages, listed under this page.

    Parameters:
    site_root: Location where the page(s) will be saved
    page_name: Name of the created page
    page_template: Template to use for the main page
    children_tmplate: Template to use for the children pages,
    page_container_id: HTML id of the `div` to be expanded with the links to the children page
    children_input_path: Where to find the ".md" files for the children
    header_getter: Function that returns the header
    """
    # read the project
    with Path(page_template).open() as data:
        html_text = data.read()
    if html_text is None:
        print("ERROR opening project html")


    # for all children with a markdown description, add the project to the page's content.
    children_folder = Path(children_input_path).glob("**/*.md")
    children_file = [f for f in children_folder if f.is_file()]
    children = []
    for p in children_file:
        # read file
        with p.open() as data:
            md = data.read()
        if md is None:
            print("ERROR opening one of the project: ", p)

        # Convert the markdown as an html file
        html = markdown2.markdown(md, extras=["metadata"])

        # Save the html and the metadata in the list
        # TODO the fields of "meta" should be parsed here... And put into a struct !
        meta = html.metadata
        children.append({"html": html, "meta": meta})

    # sort the list of children and add them to the parent page
    children = sorted(children, key=lambda element: element["meta"]["priority"])

    # create container with the html elements
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    project_page = PageBuilder(
        site_root + "/", page_name, soup.find(id=page_container_id), children_template, header_getter
    )

    # for each child, add the html in the file
    for p in children:
        children_as_html = bs4.BeautifulSoup(p["html"], "html.parser")
        project_page.add_children(p["meta"], children_as_html)

    # fill the header
    header_container = soup.find(id = "header_container")
    if header_container is None: return
    parsed = bs4.BeautifulSoup(header_getter(), "html.parser")
    header_container.append(parsed)

    # Finally, save the project page
    with open(site_root + "/" + page_name + ".html", "w") as file:
        print(" --> Saving: " + site_root + "/" + page_name + ".html")
        file.write(str(soup))

