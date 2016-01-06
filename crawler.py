#!/usr/bin/env python
import feedparser
import pdfkit
import jjjjj

content = '<html>'
d = feedparser.parse('http://katekendall.com/feed/')
for i in d.entries:
    content += '<h3><a href="' + i['link'] + '">' + i['title'] + '</a></h3>\n'
    content += '<p>' + i['content'][0]['value'] + '</p>\n'
    #print i['content'][0]['value']
content += '</html>'
#print content
pdfkit.from_string(content, 'newsletter.pdf')





#pdfkit.from_string("<html> %s" % d.entries[0]['description'] + "</html>", 'out.pdf')
#pdfkit.from_string("<html> hello </html>", 'out.pdf')
#pdfkit.from_url('http://google.com', 'out.pdf')
