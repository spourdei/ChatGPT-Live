from parse import _parse_html_tag_content, _parse_result_content, _sanitize_content


# Mock the api_types
class MetaphorSearchResultMock:
    def __init__(self, content):
        self.content = content


class MetaphorSearchResponseMock:
    def __init__(self, results):
        self.results = results


# Test the _sanitize_content function
# Test the _sanitize_content function
def test_sanitize_content():
    # Test with leading and trailing characters to remove
    input_content = "/This is a test./"
    expected_output = "This is a test"
    result = _sanitize_content(input_content)
    assert result == expected_output

    # Test with no leading or trailing characters to remove
    input_content = "This is another test"
    expected_output = "This is another test"
    result = _sanitize_content(input_content)
    assert result == expected_output

    # Test with multiple characters to remove
    input_content = "...Remove these characters!!!"
    expected_output = "Remove these characters"
    result = _sanitize_content(input_content)
    assert result == expected_output

    # Test with trailing period
    input_content = "This is a sentence."
    expected_output = "This is a sentence"
    result = _sanitize_content(input_content)
    assert result == expected_output


# Test _parse_html_tag_content function
def test_parse_html_tag_content():
    # Test for a paragraph tag
    result = _parse_html_tag_content("p", "This is a test. This is another test.")
    assert result == ["This is a test", "This is another test"]

    # Test for a non-paragraph tag
    result = _parse_html_tag_content("h1", "Header 1")
    assert result == ["Header 1"]


# Test _parse_result_content function
def test_parse_result_content():
    # Test case with sample HTML content
    content = "<html><h1>Title</h1><p>Paragraph 1.</p><p>Paragraph 2.</p></html>"
    expected_result = ["Title", "Paragraph 1", "Paragraph 2"]

    # Call the function and check the result
    result = _parse_result_content(content)
    assert result == expected_result
