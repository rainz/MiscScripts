import sys
import xml.etree.ElementTree as ET

fname = sys.argv[1]
group_name = fname[:-4]
print '<group name="{0}">'.format(group_name)
tree = ET.parse(fname)
root = tree.getroot()
ns = "{http://www.opengis.net/kml/2.2}"
places = root.findall(".//{0}Placemark".format(ns))
for p in places:
    name = p.find("{0}name".format(ns))
    coords = p.find("{0}Point/{0}coordinates".format(ns))
    parts=coords.text.split(",")
    print('<item name="{0}" lat="{1}" lon="{2}"/>'.format(name.text.strip(), int(float(parts[0])*10000), int(float(parts[1])*10000)))
print('</group>')

