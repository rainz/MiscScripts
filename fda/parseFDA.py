import sys
from lxml import etree

f = open("fda.html", "rt")
#content = f.read()

htmlparser = etree.HTMLParser()
tree = etree.parse(f, htmlparser)
#tree = etree.fromstring(content)
#tree = etree.parse("fda.html")

tbl = tree.xpath("//table[contains(@class,'search-data')]")
rows = tbl[0].xpath("//tr")
row_idx = 0
for row in rows:
    row_idx += 1
    cells = row.xpath("//td")
    print row_idx,
    for cell in cells:
        if cell.text:
            print cell.text.strip(),
    print


