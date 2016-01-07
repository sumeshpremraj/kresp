#!/usr/bin/env python
import pdfkit


with open('newsletter.html', 'r') as f:
    content = f.read()

# To do: rename file as Newsletter-DATE or something similar
pdfkit.from_string(content, '/tmp/newsletter.pdf')
