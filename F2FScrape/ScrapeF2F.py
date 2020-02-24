import time
import string
import requests
import logging
from bs4 import BeautifulSoup

#&amp;
#&nbsp;
#&lsaquo;
#&rsaquo;
#&mdash;
#&copy;

def getText(url):
    try:
        url_response = requests.get(url)
        if url_response.status_code != 200:
            logging.warn("Bad response code:" + str(url_response.status_code))
            return None
    except requests.exceptions.RequestException as e:
        logging.warn("Connection error: " + e.message)
        return None
    #html_text = url_response.text.encode('ascii', 'ignore')
    #html_text = url_response.text.encode('utf-8')
    html_text = url_response.text
    soup = BeautifulSoup(html_text, "html.parser")
    contentDiv = soup.find("div", {"id": "paging_content"})
    if contentDiv:
        with open("test.txt", "w") as f:
            f.write(contentDiv.text)
        return contentDiv.text
    return None
    
def main():
    logging.basicConfig(filename='scrape.log', level=logging.WARNING)
    logging.info("Started.")
    for i in range(1, 20):
        getText("http://www.f2finterview.com/web/Cassandra/?page="+str(i))
        
#main()
x=getText("http://www.f2finterview.com/web/Cassandra/?page=1")


