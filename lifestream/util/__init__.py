#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.conf import settings
from BeautifulSoup import BeautifulSoup, Comment

import stripper

# default settings
# VALID_TAGS is a dictionary where the key is a tag name
# and the value is a list of valid attributes.
# If the attributes list is None then all attributes are allowed.
# An empty list specifies that no attributes are allowed.
VALID_TAGS = {
    'b': (),
    'blockquote': (),
    'em': (),
    'strong': (),
    'strike': (),
    'a': ('href', 'title', 'rel'),
    'i': (),
    'br': (),
    'ul': (),
    'ol': (),
    'li': (),
    'u': (),
    'p': (),
    'h1': (),
    'h2': (),
    'h3': (),
    'h4': (),
    'table': (),
    'thead': (),
    'tbody': (),
    'tfoot': (),
    'th': (),
    'td': ('colspan',),
    'tr': ('rowspan',),
    'img': ('src', 'alt', 'title', 'width', 'height'),
    'span': (),
}

def get_url_domain(url):
    """
    Get a domain from the feed url. This attempts to
    get a clean url by ignoring know subdomains used for
    serving feeds such as www, feeds, api etc.
    """
    protocol_index = url.find('://')+3 if url.find('://')!=-1 else 0
    slash_index = url.find('/', protocol_index) if url.find('/', protocol_index)!=-1 else len(url)
  
    sub_url = url[protocol_index:slash_index]
    parts = sub_url.split('.')
  
    if len(parts) > 2 and parts[0] in ('feeds','www','feedproxy','rss','gdata','api'):
        return '.'.join(parts[1:])
    else:
        return sub_url

def sanitize_html(htmlSource, encoding=None):
    """
    Clean bad html content. Currently this simply strips tags that
    are not in the VALID_TAGS setting.
    
    This function is used as a replacement for feedparser's _sanitizeHTML
    and fixes problems like unclosed tags and gives finer grained control
    over what attributes can appear in what tags.

    Returns the sanitized html content.
    """
    js_regex = re.compile(r'[\s]*(&#x.{1,7})?'.join(list('javascript')))
    valid_tags = getattr(settings, "LIFESTREAM_VALID_TAGS", VALID_TAGS)

    # Sanitize html with BeautifulSoup
    if encoding:
        soup = BeautifulSoup(htmlSource, fromEncoding=encoding)
    else:
        soup = BeautifulSoup(htmlSource)
    

    def entities(text):
        return text.replace('<','&lt;')\
                   .replace('>', '&gt;')\
                   .replace('"', '&quot;')\
                   .replace("'", '&apos;')

    # Remove html comments
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()
 
    # Sanitize html text by changing bad text to entities.
    # BeautifulSoup will do this for href and src attributes
    # on anchors and image tags but not for text.
    for text in soup.findAll(text=True):
        text.replaceWith(entities(text))

    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        else:
            tag.attrs = [(attr, js_regex.sub('', val)) for attr, val in tag.attrs
                         if attr in valid_tags[tag.name]]
     
    # Strip disallowed tags and attributes.
    return soup.renderContents().decode('utf8') 
