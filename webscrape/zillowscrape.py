import sys
import json
import requests
from bs4 import BeautifulSoup

def buildUrl(rid, rect, page):
     return "http://www.zillow.com/search/GetResults.htm?spt=homes&status=110001&lt=111101&ht=111111&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=,&yr=,&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=1&pf=1&zoom=12&rect={1}&p={2}&sort=days&search=maplist&disp=1&rid={0}&rt=7&listright=true".format(rid, rect, page)

def readUrl(rid, rect, page):
    # You can get region ID from the GetRegionChildren API

    #url = "http://www.zillow.com/search/GetResults.htm?spt=homes&status=110001&lt=111101&ht=111111&pr=,900000&mp=,3224&bd=3%2C&ba=0%2C&sf=,&lot=,&yr=,&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=1&pf=1&zoom=12&rect=-74038582,40812315,-73923741,40865821&p="+str(page)+"&sort=days&search=maplist&disp=1&rid=60540&rt=7&listright=true&photoCardsEnabled=true&isMapSearch=true&zoom=12"

    #url = "http://www.zillow.com/search/GetResults.htm?spt=homes&status=110001&lt=111101&ht=111111&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=,&yr=,&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=1&pf=1&zoom=12&rect=-74038582,40812315,-73923741,40865821&p="+str(page)+"&sort=days&search=maplist&disp=1&rid=60540&rt=7&listright=true"

    url = buildUrl(rid, rect, page)

    #referer = "http://www.zillow.com/homes/for_sale/Fort-Lee-NJ-07024/60540_rid/3-_beds/0-900000_price/0-3224_mp/any_days/40.865821,-73.923741,40.812315,-74.038582_rect/12_zm/"

    #referer = "http://www.zillow.com/homes/for_sale/Fort-Lee-NJ-07024/house,apartment_duplex,townhouse_type/60540_rid/3-_beds/0-900000_price/0-3224_mp/any_days/40.866016,-73.923826,40.81251,-74.038668_rect/12_zm/"

    referer = "http://www.zillow.com/"

    r = requests.get(url, headers={'referer': referer})
    #print(r.status_code)
    html_doc = r.text
    return html_doc

def getAllPages(rid, rect):
    currPage = 1
    pageCount = 1
    while currPage <= pageCount:
        #print("Getting page {0}".format(currPage), file=sys.stderr)
        print >> sys.stderr, "Getting page {0}".format(currPage)
        json_txt = readUrl(rid, rect, currPage)
        try:
            json_data = json.loads(json_txt)
        except:
            #print("Error decoding json:", file=sys.stderr)
            #print(json_txt, file=sys.stderr)
            print >> sys.stderr, "Error decoding json:"
            print >> sys.stderr, json_txt
            sys.exit(-1)
        pageCount = int(json_data["list"]["numPages"])
        pageNo = int(json_data["list"]["page"])
        assert (pageNo == currPage), "pageNo {0} != currPage {1}".format(pageNo, currPage)
        processJson(json_data)
        currPage += 1


def processJson(json_data):
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

#html_file = open("zillow.json", "r")
#json_txt = html_file.read()

#json_txt = readUrl(60540, "-74038582,40812315,-73923741,40865821", 1)
#json_data = json.loads(json_txt)
#processJson(json_data)

getAllPages(60540, "-74038582,40812315,-73923741,40865821")
