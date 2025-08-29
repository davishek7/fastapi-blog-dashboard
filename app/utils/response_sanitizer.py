import bleach

allowed_tags = [
    "b",
    "i",
    "em",
    "strong",
    "u",
    "a",
    "p",
    "br",
    "ul",
    "ol",
    "li",
    "h1",
    "h2",
    "h3",
    "blockquote",
    "code",
    "pre",
]

allowed_attrs = {"a": ["href", "title", "target", "rel"]}


def strip_html(text: str) -> str:
    return bleach.clean(
        text or "", tags=allowed_tags, attributes=allowed_attrs, strip=True
    )
