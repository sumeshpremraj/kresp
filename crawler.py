#!/usr/bin/env python
import feedparser
import pdfkit
d = feedparser.parse('http://katekendall.com/feed/')
#pdfkit.from_string("<html> %s" % d.entries[0]['description'] + "</html>", 'out.pdf')
#pdfkit.from_string("<html> hello </html>", 'out.pdf')
pdfkit.from_url('http://google.com', 'out.pdf')
print d.entries[0]['title']
print d.entries[0]['description']
