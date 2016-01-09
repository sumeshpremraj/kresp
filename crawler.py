#!/usr/bin/env python
import feedparser
import mysql.connector
import re
from dateutil.parser import parse

db=mysql.connector.connect(database="kresp",user='kresp')
#query='insert into content (links,description) VALUES ("hello","hi")'
cursor=db.cursor(buffered = True)
insert_cursor=db.cursor(buffered = True)
all_links_query='select category_id,feed_url,last_updated from category_mapping'
cursor.execute(all_links_query)
for (category_id,feed_url) in cursor:
	print str(category_id) + " - " + feed_url
	#cursor.execute(query)
	# content = '<html>'
	d = feedparser.parse(feed_url)
	for i in d.entries:
		print re.escape(i['link']) + "\n" 
		print re.escape(i['title']) + "\n" 
		print i.published + "\n"
		insert_content_query='insert into content (category_id,link,title,description,publish_date) VALUES (%d,"%s","%s","%s","%s")' % (category_id,re.escape(i['link']),re.escape(i['title']),re.escape(i['description']),parse(i.published).strftime('%Y-%m-%d %H:%M:%S'))
		print insert_content_query
		insert_cursor.execute(insert_content_query)
		#     content += '<h3><a href="' + i['link'] + '">' + i['title'] + '</a></h3>'
		#     content += '<p>' + i['content'][0]['value'] + '</p>'
		#     print str(type(i['link'])) + "\n" + i['link'] + "\n" + str(type(i['description'])) + "\n" + i['description']
		#     query='insert into content (links,description) VALUES ("%s","%s")' % (re.escape(i['link']),re.escape(i['description']))
		#     cursor.execute(query)
		# content += '</html>'
db.commit()
cursor.close()
insert_cursor.close()
db.close()

