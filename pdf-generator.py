#!/usr/bin/env python
import pdfkit
import feedparser
import mysql.connector
import re
from os import environ

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



import smtplib
import base64
filename = "/tmp/newsletter.pdf"
sender = "kindlefellas@gmail.com"
recipient = "sumeshpremraj@kindle.com"

# Read a file and encode it into base64 format
fo = open(filename, "rb")
filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)

marker = "001a113ec99464560f0528e638f8"

body ="""
Newsletter for DATE
"""

# Define the main headers.
part1 = """From: Sumesh <%s>
To: Su <%s>
Subject: Newsletter
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s

--%s
""" % (sender, recipient, marker, marker)

# Define the message action
part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

# Define the attachment section
part3 = """Content-Type: application/pdf; name=\"newsletter.pdf\"
Content-Disposition: attachment; filename=\"newsletter.pdf\"
Content-Transfer-Encoding: base64

%s
--%s--
""" %(encodedcontent, marker)
message = part1 + part2 + part3

print message

try:
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.starttls()
    smtpObj.login("kindlefellas@gmail.com", environ.get('PASS'))
    #smtpObj.sendmail("kindlefellas@gmail.com", "sumesh.p@onlyfordemo.com", message)
    smtpObj.sendmail(sender, recipient, message)
    print "Successfully sent email"
except Exception:
    print "Error: unable to send email"
