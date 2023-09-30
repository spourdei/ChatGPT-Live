import typing
import re
from api_types import MetaphorSearchResult, MetaphorSearchResponse
from bs4 import BeautifulSoup


def _sanitize_content(content: str) -> str:
    # Define a regular expression pattern to match leading characters to remove
    leading_pattern = r'^[\\/.!?,;\'"()\[\]{}<>]+'

    # Use the re.sub() function to remove the matched leading characters
    content = re.sub(leading_pattern, "", content)

    # Define a regular expression pattern to match trailing characters to remove
    trailing_pattern = r'[\\/.!?,;\'"()\[\]{}<>]+$'

    # Use the re.sub() function to remove the matched trailing characters
    content = re.sub(trailing_pattern, "", content)

    return content


def _parse_html_tag_content(tag: str, content: str) -> typing.List[str]:
    # For non text tags, we will return the whole text. For longer texts, we will break them
    # into sentences since our embedding model is pretty limited
    if tag in ["p", "blockquote"]:
        # Splitting at ". " to catch sentences and not things like etc.
        return [_sanitize_content(c) for c in content.split(". ")]

    return [_sanitize_content(content)]


def _parse_result_content(content: str) -> typing.List[str]:
    # Parse the HTML content of each URL
    soup = BeautifulSoup(content, "html.parser")
    parsed_results: typing.List[str] = []

    # We are only interested in getting the content of these selectors because they are the most likely to contain
    # relevant information. In the future these can be further extended
    for selector in ["h1", "h2", "h3", "h4", "h5", "p", "b", "blockquote", "code"]:
        if elements := soup.find_all(selector):
            # Iterate over all the elements and prepare their content for the
            # embeddings
            for element in elements:
                parsed_results.extend(
                    _parse_html_tag_content(tag=selector, content=element.get_text())
                )

    return parsed_results


def parse_search_response_contents(extract: str) -> typing.List[str]:
    return _parse_result_content(extract)
