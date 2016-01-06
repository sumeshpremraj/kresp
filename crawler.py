#!/usr/bin/python
d = feedparser.parse('http://katekendall.com/feed/')
print d.entries[0]['title']
print d.entries[0]['description']
