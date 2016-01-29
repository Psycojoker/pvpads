import os
import sys
import markdown

from urllib2 import urlopen
from bs4 import BeautifulSoup

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

    preprocessed_text = preprocessor.parse(pad.content.decode("Utf-8"))
    return parser.parse(preprocessed_text.leaves()).value.replace("<body>", "").replace("</body>", "")


def etherpad(pad):
    try:
        html = urlopen(os.path.join(pad.url, "export/html")).read()
        soup = BeautifulSoup(html, "html5lib")
        return ''.join(map(unicode, soup.body.contents))
    except Exception:
        from ipdb import set_trace; set_trace()
        import traceback
        traceback.print_exc(file=sys.stdout)
        print("Error: can't fetch the html content of %s" % pad.url)
        return ""


FORMATTERS = {
    'markdown': ('Markdown', lambda pad: markdown.markdown(pad.content)),
    'mediawiki':  ('MediaWiki', mediawiki),
    'etherpad':  ('EtherPad', etherpad),
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
