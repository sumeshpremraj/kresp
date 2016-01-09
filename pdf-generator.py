#!/usr/bin/env python
import pdfkit
import feedparser
import mysql.connector
import re

db=mysql.connector.connect(database="kresp",user='kresp')
category_cursor=db.cursor(buffered = True)
user_cursor=db.cursor(buffered = True)
content_cursor=db.cursor(buffered=True)
user_query='select kindle_id,category_ids from user'
user_cursor.execute(user_query)
print user_cursor
for (kindle_id,category_ids) in user_cursor:
    print kindle_id
    cats = category_ids.split(",")
    for i in cats:
    	content_query = "select link,description from content where category_id = %s" %i
    	content_cursor.execute(content_query)
    	for (link,description) in content_cursor:
    		print link + "\n" + description

#for (category_id,feed_url) in cursor:
#	print str(category_id) + " - " + feed_url
#	d = feedparser.parse(feed_url)
#	for i in d.entries:
#		insert_content_query='insert into content (category_id,link,title,description) VALUES (%d,"%s","%s","%s")' % (category_id,re.escape(i['link']),re.escape(i['title']),re.escape(i['description']))
#		print insert_content_query
#		insert_cursor.execute(insert_content_query)
#db.commit()
user_cursor.close()
db.close()

		#     content += '<h3><a href="' + i['link'] + '">' + i['title'] + '</a></h3>'
		#     content += '<p>' + i['content'][0]['value'] + '</p>'
		#     print str(type(i['link'])) + "\n" + i['link'] + "\n" + str(type(i['description'])) + "\n" + i['description']
		#     query='insert into content (links,description) VALUES ("%s","%s")' % (re.escape(i['link']),re.escape(i['description']))
		#     cursor.execute(query)
		# content += '</html>'

# To do: rename file as Newsletter-DATE or something similar
#pdfkit.from_string(content, '/tmp/newsletter.pdf')

