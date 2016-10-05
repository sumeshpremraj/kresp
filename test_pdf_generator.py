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
div.header {width: 700px; padding: 0px; margin: 25px auto 30px; text-align: center; font-family: Arial, sans-serif; color:#555}
div.container { width: 700px; padding: 20px; margin: 0 auto; }
div.container div {margin-bottom:10px ; padding: 10px 15px;border-bottom:1px solid #ccc}
div.container div a { color: #1e3e7b; text-decoration: none; border-bottom: 1px solid #ccc; }
div.clear{display:none;}
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

feed_url="https://xkcd.com/rss.xml"
d = feedparser.parse(feed_url)
for i in d.entries:
        print i['link'] + "\n"
        print i['title'] + "\n"
        print i['description']

count = 1
for i in d.entries:
                #print link + title + description
            if count%2 == 1:
                divclass = "left"
            else:
                divclass = "right"
            content += '<div class="' + divclass + '">'
            content += '<h4><a href="' + i['link'] + '">' + i['title'] + '</a></h4>'
            content += '<p>' + i['description'] + '</p></div>'

            if count%2 == 0:
                content += '<div class="clear"></div>'

            count = count+1

pdfkit.from_string(content, 'newsletter.pdf')
