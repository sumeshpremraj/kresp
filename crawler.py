#!/usr/bin/env python
import feedparser
import pdfkit
import mysql.connector
import re

db=mysql.connector.connect(database="kresp",user='satya.singh')
query='insert into content (links,description) VALUES ("hello","hi")'
cursor=db.cursor()
cursor.execute(query)
content = '<html>'
d = feedparser.parse('http://katekendall.com/feed/')
for i in d.entries:
    content += '<h3><a href="' + i['link'] + '">' + i['title'] + '</a></h3>'
    content += '<p>' + i['content'][0]['value'] + '</p>'
    print str(type(i['link'])) + "\n" + i['link'] + "\n" + str(type(i['description'])) + "\n" + i['description']
    #query="insert into content (links,description) VALUES (str(i['link']),str(i['description']))"
    query='insert into content (links,description) VALUES ("%s","%s")' % (re.escape(i['link']),re.escape(i['description']))
    #print query
    cursor.execute(query)
    #print i['content'][0]['value']
content += '</html>'
db.commit()
cursor.close()
db.close()
#print content
pdfkit.from_string(content, 'newsletter.pdf')





#pdfkit.from_string("<html> %s" % d.entries[0]['description'] + "</html>", 'out.pdf')
#pdfkit.from_string("<html> hello </html>", 'out.pdf')
#pdfkit.from_url('http://google.com', 'out.pdf')
