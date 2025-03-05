from django.template import Library
from django.template.defaultfilters import stringfilter
from markdown import markdown as markdown_

register = Library()


@register.filter
@stringfilter
def markdown(value: str) -> str:
    return markdown_(value)
