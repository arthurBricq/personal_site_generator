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


def _parse_keywords(value):
    """'[Chess, Rust]' -> ['Chess', 'Rust']."""
    return [k.strip() for k in value.strip().strip("[]").split(",") if k.strip()]


GITHUB_ICON = (
    '<svg viewBox="0 0 16 16" width="1em" height="1em" fill="currentColor" aria-hidden="true">'
    '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
    '0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53'
    '.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 '
    '0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 '
    '2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 '
    '3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
)

YOUTUBE_ICON = (
    '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="currentColor" aria-hidden="true">'
    '<path d="M23.5 6.2a3 3 0 00-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 00.5 6.2 '
    '31.3 31.3 0 000 12a31.3 31.3 0 00.5 5.8 3 3 0 002.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 '
    '002.1-2.1A31.3 31.3 0 0024 12a31.3 31.3 0 00-.5-5.8zM9.5 15.5v-7l6.5 3.5-6.5 3.5z"/></svg>'
)


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

        # Give each child page its own SEO title and description
        title_tag = template.find("title")
        if title_tag is not None:
            title_tag.string = _meta["title"]
        desc_tag = template.find("meta", attrs={"name": "description"})
        if desc_tag is not None and "description" in _meta:
            desc_tag["content"] = _meta["description"]

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
        slug = _process_children_page_title(_meta)
        href = "./{}/{}.html".format(self._name, slug)

        # --- left column: title, date, tags, description, links ---
        main = '<a class="card_title" href="{}">{}</a>'.format(href, _meta["title"])

        dates = _format_dates(_meta)
        if dates:
            main += '<span class="card_date">{}</span>'.format(dates)

        # wrap title + date on one baseline row
        main = '<div class="card_head">{}</div>'.format(main)

        if "keywords" in _meta:
            tags = "".join(
                '<li class="tag">{}</li>'.format(k)
                for k in _parse_keywords(_meta["keywords"])
            )
            main += '<ul class="tags">{}</ul>'.format(tags)

        main += '<p class="description">{}</p>'.format(_meta["description"])

        links = ""
        if "github" in _meta:
            links += '<a class="icon_link" href="{}">{}GitHub</a>'.format(
                _meta["github"], GITHUB_ICON
            )
        if "youtube" in _meta:
            links += '<a class="icon_link" href="{}">{}YouTube</a>'.format(
                _meta["youtube"], YOUTUBE_ICON
            )
        if links:
            main += '<div class="card_links">{}</div>'.format(links)

        # --- right column: thumbnail (optional) ---
        thumb = ""
        if "featuredImage" in _meta:
            thumb = '<a class="card_thumb" href="{}"><img src="{}" alt="{}"></a>'.format(
                href, _meta["featuredImage"], _meta["title"]
            )

        html = '<div class="card card_{}"><div class="card_main">{}</div>{}</div>'.format(
            self._name, main, thumb
        )

        tag = bs4.BeautifulSoup(html, "html.parser")
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

    # sort the list of children: highest priority first
    children = sorted(children, key=lambda element: int(element["meta"]["priority"]), reverse=True)

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

