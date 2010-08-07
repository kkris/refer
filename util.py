#!/usr/bin/env python

import re

_punct_re = re.compile(r'''[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+''')

def slugify(text, delim=u'-'):
    '''
    Taken from http://flask.pocoo.org/snippets/5/
    Generates an ASCII-only slug.
    '''
    result = []
    for word in _punct_re.split(text.lower()):
        if word:
            result.append(word)
    return unicode(delim.join(result))


def convert_datetime(post):
    post['time'] = post['time'].strftime('%d %b %Y %H:%M')
    return post
