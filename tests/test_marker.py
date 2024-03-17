import unittest

from src import marker


class TestHighLevelTokenizer(unittest.TestCase):

    def test_title_h1(self):
        # Arrange
        input = ["# This is a test"]
        expected = [["H1", "This is a test"]]
        # Act
        tokens = marker.high_level_tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_title_h2(self):
        # Arrange
        input = ["## This is a test"]
        expected = [["H2", "This is a test"]]
        # Act
        tokens = marker.high_level_tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_title_h3(self):
        # Arrange
        input = ["### This is a test"]
        expected = [["H3", "This is a test"]]
        # Act
        tokens = marker.high_level_tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_title_h4(self):
        # Arrange
        input = ["#### This is a test"]
        expected = [["H4", "This is a test"]]
        # Act
        tokens = marker.high_level_tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_title_h5(self):
        tokens = marker.high_level_tokenizer(["##### This is a test"])
        expected = [["H5", "This is a test"]]
        self.assertEqual(expected, tokens)

    def test_paragraph(self):
        tokens = marker.high_level_tokenizer(["This is a test"])
        expected = [[marker.PARAGRAPH, "This is a test"]]
        self.assertEqual(expected, tokens)

    def test_breakline(self):
        tokens = marker.high_level_tokenizer(["\n"])
        self.assertEqual([[marker.BREAKLINE, "\n"]], tokens)

    def test_all_identifiers(self):
        # Arrange
        input = [
            "# H1\n",
            "## H2\n",
            "### H3\n",
            "#### H4\n",
            "##### H5\n",
            "###### H6\n",
            "This is a test\n",
            "\n",
        ]
        expected = [
            [marker.H1, "H1\n"],
            [marker.H2, "H2\n"],
            [marker.H3, "H3\n"],
            [marker.H4, "H4\n"],
            [marker.H5, "H5\n"],
            [marker.H6, "H6\n"],
            [marker.PARAGRAPH, "This is a test\n"],
            [marker.BREAKLINE, "\n"],
        ]
        # Act
        tokens = marker.high_level_tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_all_identifiers_with_links(self):
        # Arrange
        input = [
            "# H1\n",
            "## H2\n",
            "### H3\n",
            "#### H4\n",
            "##### H5\n",
            "###### H6\n",
            "This is a test [my-link](https://link.com)\n",
            "\n",
        ]
        expected = [
            [marker.H1, "H1\n"],
            [marker.H2, "H2\n"],
            [marker.H3, "H3\n"],
            [marker.H4, "H4\n"],
            [marker.H5, "H5\n"],
            [marker.H6, "H6\n"],
            [marker.PARAGRAPH, "This is a test [my-link](https://link.com)\n"],
            [marker.BREAKLINE, "\n"],
        ]
        # Act
        tokens = marker.high_level_tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)


class TestParseLinks(unittest.TestCase):
    def test_parse_link(self):
        # Arrange
        input = "This is a test [my-link](https://link.com)"
        expected = [
            [marker.TEXT, "This is a test "],
            [marker.LINK, "https://link.com", "my-link"],
            [marker.TEXT, ""],
        ]
        # Act
        tokens = marker.parse_links(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_parse_link_inner_bracket(self):
        # Arrange
        input = "This is a test [[my-link]](https://link.com)"
        expected = [
            [marker.TEXT, "This is a test "],
            [marker.LINK, "https://link.com", "[my-link]"],
            [marker.TEXT, ""],
        ]
        # Act
        tokens = marker.parse_links(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_parse_link_inner_bracket_inner_parentheses(self):
        # Arrange
        input = "This is a test [[my-link]]((https://link.com))"
        expected = [
            [marker.TEXT, "This is a test "],
            [marker.LINK, "(https://link.com", "[my-link]"],
            [marker.TEXT, ")"],
        ]
        # Act
        tokens = marker.parse_links(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_parse_link_extra_left_bracket(self):
        # Arrange
        input = "This is a test [[my-link](https://link.com)))"
        expected = [
            [marker.TEXT, "This is a test "],
            [marker.LINK, "https://link.com", "[my-link"],
            [marker.TEXT, "))"],
        ]
        # Act
        tokens = marker.parse_links(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_parse_link_empty_link(self):
        # Arrange
        input = "[]()"
        expected = [[marker.LINK, "", ""], [marker.TEXT, ""]]
        # Act
        tokens = marker.parse_links(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_parse_link_two_links(self):
        # Arrange
        input = "[link1](https://link1) [link2](https://link2)"
        expected = [
            [marker.LINK, "https://link1", "link1"],
            [marker.TEXT, " "],
            [marker.LINK, "https://link2", "link2"],
            [marker.TEXT, ""],
        ]
        # Act
        tokens = marker.parse_links(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_parse_link_inner_bracket_join(self):
        # Arrange
        input = "[link1](https://link1)[link2](https://link2)"
        tokens = marker.parse_links(input)
        # Assert
        expected = [
            [marker.LINK, "https://link1", "link1"],
            [marker.LINK, "https://link2", "link2"],
            [marker.TEXT, ""],
        ]
        # Act
        self.assertEqual(expected, tokens)

    def test_parse_link_inner_bracket_join_repetions(self):
        # Arrange
        input = "[link1](https://link1)[link2](https://link2)*[link3](https://link3)"
        expected = [
            [marker.LINK, "https://link1", "link1"],
            [marker.LINK, "https://link2", "link2"],
            [marker.TEXT, "*"],
            [marker.LINK, "https://link3", "link3"],
            [marker.TEXT, ""],
        ]
        # Act
        tokens = marker.parse_links(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_parse_link_start_chars(self):
        # Arrange
        input = (
            "starts[link1](https://link1)[link2](https://link2)[link3](https://link3)"
        )
        expected = [
            [marker.TEXT, "starts"],
            [marker.LINK, "https://link1", "link1"],
            [marker.LINK, "https://link2", "link2"],
            [marker.LINK, "https://link3", "link3"],
            [marker.TEXT, ""],
        ]
        # Act
        tokens = marker.parse_links(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_parse_link_remainder_chars(self):
        # Arrange
        input = "[link1](https://link1)[link2](https://link2)*[link3](https://link3)remainder"
        expected = [
            [marker.LINK, "https://link1", "link1"],
            [marker.LINK, "https://link2", "link2"],
            [marker.TEXT, "*"],
            [marker.LINK, "https://link3", "link3"],
            [marker.TEXT, "remainder"],
        ]
        # Act
        tokens = marker.parse_links(input)
        # Assert
        self.assertEqual(expected, tokens)


class TestTokenizer(unittest.TestCase):
    def test_tokenizer_h1_with_link(self):
        # Arrange
        input = ["# This is a header with [my-link](https://link.com)"]
        expected = [
            [
                marker.H1,
                [
                    [marker.TEXT, "This is a header with "],
                    [marker.LINK, "https://link.com", "my-link"],
                    [marker.TEXT, ""],
                ],
            ]
        ]
        # Act
        tokens = marker.tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_tokenizer_default_paragraph_and_link(self):
        # Arrange
        input = ["This is a test [my-link](https://link.com)"]
        expected = [
            [
                marker.PARAGRAPH,
                [
                    [marker.TEXT, "This is a test "],
                    [marker.LINK, "https://link.com", "my-link"],
                    [marker.TEXT, ""],
                ],
            ]
        ]
        # Act
        tokens = marker.tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_tokenizer_not_a_header(self):
        # Arrange
        input = ["######## This is not a header but a paragraph"]
        expected = [
            [
                marker.PARAGRAPH,
                [[marker.TEXT, "######## This is not a header but a paragraph"]],
            ]
        ]
        # Act
        tokens = marker.tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_tokenizer_h1_and_link(self):
        # Arrange
        input = ["# H1", "This is a test [my-link](https://link.com)"]
        expected = [
            [marker.H1, [[marker.TEXT, "H1"]]],
            [
                marker.PARAGRAPH,
                [
                    [marker.TEXT, "This is a test "],
                    [marker.LINK, "https://link.com", "my-link"],
                    [marker.TEXT, ""],
                ],
            ],
        ]
        # Act
        tokens = marker.tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_tokenizer_h6_and_link(self):
        # Arrange
        input = ["###### H6", "This is a test [my-link](https://link.com)"]
        expected = [
            [marker.H6, [[marker.TEXT, "H6"]]],
            [
                marker.PARAGRAPH,
                [
                    [marker.TEXT, "This is a test "],
                    [marker.LINK, "https://link.com", "my-link"],
                    [marker.TEXT, ""],
                ],
            ],
        ]
        # Act
        tokens = marker.tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)

    def test_tokenizer_as_read_in_file_all_headers_paragraph_with_links(self):
        # Arrange
        input = [
            "# H1\n",
            "## H2\n",
            "### H3\n",
            "#### H4\n",
            "##### H5\n",
            "###### H6\n",
            "This is a test [my-link](https://link.com)\n",
            "\n",
        ]
        expected = [
            [marker.H1, [["TEXT", "H1\n"]]],
            [marker.H2, [["TEXT", "H2\n"]]],
            [marker.H3, [["TEXT", "H3\n"]]],
            [marker.H4, [["TEXT", "H4\n"]]],
            [marker.H5, [["TEXT", "H5\n"]]],
            [marker.H6, [["TEXT", "H6\n"]]],
            [
                marker.PARAGRAPH,
                [
                    ["TEXT", "This is a test "],
                    [marker.LINK, "https://link.com", "my-link"],
                    ["TEXT", "\n"],
                ],
            ],
            [marker.BREAKLINE, [["TEXT", "\n"]]],
        ]
        # Act
        tokens = marker.tokenizer(input)
        # Assert
        self.assertEqual(expected, tokens)


class TestIdentifyHeaderSize(unittest.TestCase):
    def test_identify_no_header(self):
        # Arrange
        input = "######## This is a test"
        expected = []
        # Act
        result = marker.identify_header_size(input)
        # Assert
        self.assertEqual(expected, result)

    def test_identify_header_size_h1(self):
        # Arrange
        input = "# H1"
        expected = [marker.H1, "H1"]
        # Act
        result = marker.identify_header_size(input)
        # Assert
        self.assertEqual(expected, result)

    def test_identify_header_size_h2(self):
        # Arrange
        input = "## H2"
        expected = [marker.H2, "H2"]
        # Act
        result = marker.identify_header_size(input)
        # Assert
        self.assertEqual(expected, result)

    def test_identify_header_size_h3(self):
        # Arrange
        input = "### H3"
        expected = [marker.H3, "H3"]
        # Act
        result = marker.identify_header_size(input)
        # Assert
        self.assertEqual(expected, result)

    def test_identify_header_size_h4(self):
        # Arrange
        input = "#### H4"
        expected = [marker.H4, "H4"]
        # Act
        result = marker.identify_header_size(input)
        # Assert
        self.assertEqual(expected, result)

    def test_identify_header_size_h5(self):
        # Arrange
        input = "##### H5"
        expected = [marker.H5, "H5"]
        # Act
        result = marker.identify_header_size(input)
        # Assert
        self.assertEqual(expected, result)

    def test_identify_header_size_h6(self):
        # Arrange
        input = "###### H6"
        expected = [marker.H6, "H6"]
        # Act
        result = marker.identify_header_size(input)
        # Assert
        self.assertEqual(expected, result)


class HtmlGenerator(unittest.TestCase):
    def test_html_generstor_h1(self):
        # Arrange
        parsed_tokens = [[marker.H1, [[marker.TEXT, "H1"]]]]
        expected = "<h1>H1</h1>"
        # Act
        result = marker.html_generator(parsed_tokens)
        # Assert
        self.assertEqual(expected, result)

    def test_html_generator_allheader(self):
        # Arrange
        parsed_tokens = [
            [marker.H1, [[marker.TEXT, "H1"]]],
            [marker.H2, [[marker.TEXT, "H2"]]],
            [marker.H3, [[marker.TEXT, "H3"]]],
            [marker.H4, [[marker.TEXT, "H4"]]],
            [marker.H5, [[marker.TEXT, "H5"]]],
            [marker.H6, [[marker.TEXT, "H6"]]],
        ]
        expected = "<h1>H1</h1><h2>H2</h2><h3>H3</h3><h4>H4</h4><h5>H5</h5><h6>H6</h6>"
        # Act
        result = marker.html_generator(parsed_tokens)
        # Assert
        self.assertEqual(expected, result)
    
    def test_html_generator_paragraph(self):
        # Arrange
        parsed_tokens = [
            [marker.PARAGRAPH, [[marker.TEXT, "This is a first test"]]],
            [marker.PARAGRAPH, [[marker.TEXT, "This is a second test"]]]
        ]
        expected = "<p>This is a first test</p><p>This is a second test</p>"
        # Act
        result = marker.html_generator(parsed_tokens)
        # Assert
        self.assertEqual(expected, result)
    
    def test_html_generator_link(self):
        # Arrange
        parsed_tokens = [
            [marker.PARAGRAPH, [[marker.LINK, "https://link.com", "my-link"]]]
        ]
        expected = '<p><a href="https://link.com">my-link</a></p>'
        # Act
        result = marker.html_generator(parsed_tokens)
        # Assert
        self.assertEqual(expected, result)
    
    def test_html_generator_link_and_text(self):
        # Arrange
        parsed_tokens = [
            [marker.PARAGRAPH, 
                [
                    [marker.TEXT, "This is a test "],
                    [marker.LINK, "https://link.com", "my-link"],
                    [marker.TEXT, ""]
                ]
            ]
        ]
        expected = '<p>This is a test <a href="https://link.com">my-link</a></p>'
        # Act
        result = marker.html_generator(parsed_tokens)
        # Assert
        self.assertEqual(expected, result)
