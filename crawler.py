#!/usr/bin/env python
import feedparser
import mysql.connector
import re

db=mysql.connector.connect(database="kresp",user='kresp')
#query='insert into content (links,description) VALUES ("hello","hi")'
cursor=db.cursor()
#cursor.execute(query)
content = '<html>'
d = feedparser.parse('http://katekendall.com/feed/')
for i in d.entries:
    content += '<h3><a href="' + i['link'] + '">' + i['title'] + '</a></h3>'
    content += '<p>' + i['content'][0]['value'] + '</p>'
    print str(type(i['link'])) + "\n" + i['link'] + "\n" + str(type(i['description'])) + "\n" + i['description']
    query='insert into content (links,description) VALUES ("%s","%s")' % (re.escape(i['link']),re.escape(i['description']))
    cursor.execute(query)
content += '</html>'
db.commit()
cursor.close()
db.close()

