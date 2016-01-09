#!/usr/bin/env python
import pdfkit
import feedparser
import mysql.connector
import re

content = '''
<html>
<head>
<style type="text/css">
h3 { margin: 8px 0 10px; font-size: 26px}
h4 { margin: 0 0 10px; font-size: 18px}
body {background: #fff; font-family: Arial, sans-serif;}
div.header {width: 600px; padding: 0px; margin: 25px auto 30px; text-align: center; font-family: Arial, sans-serif; color:#555}
div.container { width: 600px; padding: 20px; margin: 0 auto; }
div.container div {width: 250px; margin-right: 10px; padding: 10px 15px;background: #eee; border-radius: 8px}
div.container div a { color: #1e3e7b; text-decoration: none; border-bottom: 1px solid #ccc; }
div.container div.left { float: left }
div.container div.right { float: right; }
div.clear { visibility: hidden; clear: both;}
div.footer { width: 600px; margin: 25px auto 30px;text-align: center; color: #999}
div.footer a{color: #777}
</style>
</head>
<body>
<div class="header">
    <h3>Kindlefellas</h3>
    <h4>Your personalized newsletter</h4>
</div>

<!--  container -->
<div class="container">
'''

db=mysql.connector.connect(database="kresp",user='kresp')
category_cursor=db.cursor(buffered = True)
user_cursor=db.cursor(buffered = True)
content_cursor=db.cursor(buffered=True)
user_query='select kindle_id,category_ids from user'
user_cursor.execute(user_query)

#print user_cursor

count = 1
for (kindle_id,category_ids) in user_cursor:
    print kindle_id
    cats = category_ids.split(",")
    for i in cats:
        print "Category ID: " + i
    	content_query = "select link,title,description from content where category_id = %s " %i
    	content_cursor.execute(content_query)
    	for (link,title,description) in content_cursor:
    		#print link + title + description
            if count%2 == 1:
                divclass = "left"
            else:
                divclass = "right"
            content += '<div class="' + divclass + '">'
            content += '<h4><a href="' + link + '">' + title + '</a></h4>'
            content += '<p>' + description + '</p></div>'

            if count%2 == 0:
                content += '<div class="clear"></div>'

            count = count+1


user_cursor.close()
db.close()

content += """
</div>
<!-- /container -->
<div class="clear"></div>
<div class="footer">
<a href="#">Click here to unsubscribe</a> | Content &copy; respective authors
</div>
</body>
</html>
"""
#print content

# To do: rename file as Newsletter-DATE or something similar
pdfkit.from_string(content, '/tmp/newsletter.pdf')

#for (category_id,feed_url) in cursor:
#   print str(category_id) + " - " + feed_url
#   d = feedparser.parse(feed_url)
#   for i in d.entries:
#       insert_content_query='insert into content (category_id,link,title,description) VALUES (%d,"%s","%s","%s")' % (category_id,re.escape(i['link']),re.escape(i['title']),re.escape(i['description']))
#       print insert_content_query
#       insert_cursor.execute(insert_content_query)
#db.commit()

		#     content += '<h3><a href="' + i['link'] + '">' + i['title'] + '</a></h3>'
		#     content += '<p>' + i['content'][0]['value'] + '</p>'
		#     print str(type(i['link'])) + "\n" + i['link'] + "\n" + str(type(i['description'])) + "\n" + i['description']
		#     query='insert into content (links,description) VALUES ("%s","%s")' % (re.escape(i['link']),re.escape(i['description']))
		#     cursor.execute(query)
		# content += '</html>'