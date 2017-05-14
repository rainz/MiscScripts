import sys
import json
import requests
from bs4 import BeautifulSoup

def readUrl():
    page=1

    # You can get region ID from the GetRegionChildren API

    #url = "http://www.zillow.com/search/GetResults.htm?spt=homes&status=110001&lt=111101&ht=111111&pr=,900000&mp=,3224&bd=3%2C&ba=0%2C&sf=,&lot=,&yr=,&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=1&pf=1&zoom=12&rect=-74038582,40812315,-73923741,40865821&p="+str(page)+"&sort=days&search=maplist&disp=1&rid=60540&rt=7&listright=true&photoCardsEnabled=true&isMapSearch=true&zoom=12"

    url = "http://www.zillow.com/search/GetResults.htm?spt=homes&status=110001&lt=111101&ht=111111&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=,&yr=,&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=1&pf=1&zoom=12&rect=-74038582,40812315,-73923741,40865821&p="+str(page)+"&sort=days&search=maplist&disp=1&rid=60540&rt=7&listright=true"
    #referer = "http://www.zillow.com/homes/for_sale/Fort-Lee-NJ-07024/60540_rid/3-_beds/0-900000_price/0-3224_mp/any_days/40.865821,-73.923741,40.812315,-74.038582_rect/12_zm/"

    #referer = "http://www.zillow.com/homes/for_sale/Fort-Lee-NJ-07024/house,apartment_duplex,townhouse_type/60540_rid/3-_beds/0-900000_price/0-3224_mp/any_days/40.866016,-73.923826,40.81251,-74.038668_rect/12_zm/"

    #referer = "http://www.zillow.com/homes/for_sale/Fort-Lee-NJ-07024/house,apartment_duplex,townhouse_type/60540_rid/3-_beds/0-900000_price/0-3224_mp/any_days/"
    #referer = "http://www.zillow.com/homes/for_sale/"
    referer = "http://www.zillow.com/"

    r = requests.get(url, headers={'referer': referer})
    #print(r.status_code)
    html_doc = r.text
    #print(html_doc)
    return html_doc

def processJson(json_txt):
    json_data = json.loads(json_txt)

    pageCount = int(json_data["list"]["numPages"])
    currPage = int(json_data["list"]["page"])

    html_doc = json_data["list"]["listHTML"];
    soup = BeautifulSoup(html_doc, 'html.parser')
    results = soup.find(id="search-results").ul
    fields = {"property_type": "zsg-photo-card-status",
            "address"      : "zsg-photo-card-address",
            "price"        : "zsg-photo-card-price",
            "info"         : "zsg-photo-card-info",
            #"notification" : "zsg-photo-card-notification",
            "broker"       : "zsg-photo-card-broker-name"}

    for listItem in results:
        article = listItem.article
        if not article:
            # Maybe an ad?
            continue
        print article['data-zpid'], article['data-longitude'], article['data-latitude']
        print article.find("a", {"class": "zsg-photo-card-overlay-link"})["href"] # could have "AuthRequired" for foreclosures
        captions = article.find("div", {"class": "zsg-photo-card-caption"})
        for f in fields:
            val = captions.find("span", {"class": fields[f]})
            if val is None:
                valText = "none"
            else:
                valText = val.text
            print f, valText
        print "========================================="

    #addrs = [e.text for e in addr_spans]
    #for addr in addrs:
    #  print addr

    print("Page " + str(currPage) + "/" + str(pageCount))
    print(json_data["list"]["binCounts"])

# To allow printing of unicode text
reload(sys)
sys.setdefaultencoding('utf-8')

json_txt = readUrl()
#html_file = open("zillow.json", "r")
#json_txt = html_file.read()
processJson(json_txt)
