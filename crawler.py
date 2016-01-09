#!/usr/bin/env python
import feedparser
import mysql.connector
import re
from dateutil.parser import parse
import datetime
import pytz

db=mysql.connector.connect(database="kresp",user='kresp')
#query='insert into content (links,description) VALUES ("hello","hi")'
category_mapping_cursor=db.cursor(buffered = True)
update_category_mapping_cursor=db.cursor(buffered = True)
all_links_query='select id,category_id,feed_url,last_updated from category_mapping'
category_mapping_cursor.execute(all_links_query)
print category_mapping_cursor.rowcount
content_cursor=db.cursor(buffered = True)
for (id,category_id,feed_url,last_updated) in category_mapping_cursor:
	print id
	latest_update=pytz.utc.localize(last_updated) if last_updated is not None else datetime.datetime(1970,1,1,0,0,0,tzinfo=pytz.utc)
	#latest_update=datetime.datetime(1970,1,1,0,0,0,tzinfo=pytz.utc)
	print latest_update
	print str(category_id) + " - " + feed_url
	dateset=[]
	#cursor.execute(query)
	# content = '<html>'
	d = feedparser.parse(feed_url)
	for i in d.entries:
		print re.escape(i['link']) + "\n" 
		print re.escape(i['title']) + "\n" 
		item_publish_date = parse(i.published)	
		print type(item_publish_date)
		print type(latest_update)
		if latest_update < item_publish_date :
			insert_content_query='insert into content (category_id,link,title,description,publish_date) VALUES (%d,"%s","%s","%s","%s")' % (category_id,re.escape(i['link']),re.escape(i['title']),re.escape(i['description']),item_publish_date.strftime('%Y-%m-%d %H:%M:%S'))
			print insert_content_query
			content_cursor.execute(insert_content_query)
			dateset.append(item_publish_date)
		#     content += '<h3><a href="' + i['link'] + '">' + i['title'] + '</a></h3>'
		#     content += '<p>' + i['content'][0]['value'] + '</p>'
		#     print str(type(i['link'])) + "\n" + i['link'] + "\n" + str(type(i['description'])) + "\n" + i['description']
		#     query='insert into content (links,description) VALUES ("%s","%s")' % (re.escape(i['link']),re.escape(i['description']))
		#     cursor.execute(query)
		# content += '</html>'
	print dateset
	if dateset:
		update_last_publish_date_query="update category_mapping set last_updated='%s' where id = %d" % (max(dateset).strftime('%Y-%m-%d %H:%M:%S'),id)
		update_category_mapping_cursor.execute(update_last_publish_date_query)
		print update_last_publish_date_query
db.commit()
category_mapping_cursor.close()
content_cursor.close()
db.close()

