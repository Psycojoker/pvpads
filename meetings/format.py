import markdown

from mediawiki_parser.preprocessor import make_parser
from mediawiki_parser.html import make_parser as make_html_parser


def mediawiki(pad):
    templates = {}
    allowed_tags = []
    allowed_self_closing_tags = []
    allowed_attributes = []
    interwiki = {}
    namespaces = {}

    preprocessor = make_parser(templates)

    parser = make_html_parser(allowed_tags, allowed_self_closing_tags, allowed_attributes, interwiki, namespaces)

    preprocessed_text = preprocessor.parse(pad.content)
    return parser.parse(preprocessed_text.leaves()).value.replace("<body>", "").replace("</body>", "")


FORMATTERS = {
    'markdown': ('Markdown', lambda pad: markdown.markdown(pad.content)),
    'mediawiki':  ('MediaWiki', mediawiki),
}

FORMATS = ((x[0], x[1][0]) for x in FORMATTERS.items())

# built from here https://www.w3.org/TR/html-markup/elements.html
ALLOWED_TAGS = (
    "a",
    "abbr",
    "b",
    "blockquote",
    "br",
    "col",
    "colgroup",
    "dd",
    "del",
    "div",
    "dl",
    "dt",
    "em",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hgroup",
    "hr",
    "i",
    "img",
    "label",
    "legend",
    "li",
    "nav",
    "ol",
    "p",
    "pre",
    "q",
    "section",
    "small",
    "span",
    "strong",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "u",
    "ul",
    "wbr",
)
