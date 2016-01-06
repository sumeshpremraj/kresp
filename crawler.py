#!/usr/bin/env python
import feedparser
import pdfkit
content = '<html>'
d = feedparser.parse('http://katekendall.com/feed/')
for i in d.entries:
    content += '<h3><a href="' + i['link'] + '>' + i['title'] + '</a></h3>\n'
    content += '<p>' + i['description'] + '</p>\n'
content += '</html>'
#print content

pdfkit.from_string(content, 'out.pdf')

#pdfkit.from_string("<html> %s" % d.entries[0]['description'] + "</html>", 'out.pdf')
#pdfkit.from_string("<html> hello </html>", 'out.pdf')
#pdfkit.from_url('http://google.com', 'out.pdf')
