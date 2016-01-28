import markdown


FORMATTERS = {
    'markdown': ('Markdown', lambda pad: markdown.markdown(pad.content)),
}

FORMATS = ((x[0], x[1][0]) for x in FORMATTERS.items())
