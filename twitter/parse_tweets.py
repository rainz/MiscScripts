#!/usr/bin/python

import sys
import json
import datetime

file_name = "tw_small.txt"
if len(sys.argv) > 1:
  file_name = sys.argv[1]
tweet_file = open(file_name, "r")
for twt in tweet_file:
  js = json.loads(twt)
  js_timestamp = js.get("timestamp_ms")
  if js_timestamp:
    js_timestamp = long(js_timestamp)/1000
  else:
    js_timestamp = 0
  js_user = js.get("user")
  js_lang = js.get("lang")
  if not js_lang:
    js_lang = "Unknown"
  js_text = js.get("text")
  if not js_text:
    js_text = ""
  js_geo = js.get("geo")
  js_coords = None
  if js_geo:
    js_coords = js_geo.get("coordinates")
  js_place = js.get("place")

  if js_place and js_lang == "en":
    print datetime.datetime.fromtimestamp(js_timestamp).strftime('%Y-%m-%d %H:%M:%S'), 
    print ": (" + js_user["screen_name"] + ", " + js_place["full_name"] + ")", js_text
