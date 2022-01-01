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

def accent2htmlcode():
    htmlcodes = ['&Aacute;', '&aacute;', '&Agrave;', '&Acirc;', '&agrave;', '&Acirc;', '&acirc;', '&Auml;', '&auml;', '&Atilde;', '&atilde;', '&Aring;', '&aring;', '&Aelig;', '&aelig;', '&Ccedil;', '&ccedil;', '&Eth;', '&eth;', '&Eacute;', '&eacute;', '&Egrave;', '&egrave;', '&Ecirc;', '&ecirc;', '&Euml;', '&euml;', '&Iacute;', '&iacute;', '&Igrave;', '&igrave;', '&Icirc;', '&icirc;', '&Iuml;', '&iuml;', '&Ntilde;', '&ntilde;', '&Oacute;', '&oacute;', '&Ograve;', '&ograve;', '&Ocirc;', '&ocirc;', '&Ouml;', '&ouml;', '&Otilde;', '&otilde;', '&Oslash;', '&oslash;', '&szlig;', '&Thorn;', '&thorn;', '&Uacute;', '&uacute;', '&Ugrave;', '&ugrave;', '&Ucirc;', '&ucirc;', '&Uuml;', '&uuml;', '&Yacute;', '&yacute;', '&yuml;', '&copy;', '&reg;', '&trade;', '&euro;', '&cent;', '&pound;', '&lsquo;', '&rsquo;', '&ldquo;', '&rdquo;', '&laquo;', '&raquo;', '&mdash;', '&ndash;', '&deg;', '&plusmn;', '&frac14;', '&frac12;', '&frac34;', '&times;', '&divide;', '&alpha;', '&beta;', '&infin']
    funnychars = ['\xc1','\xe1','\xc0','\xc2','\xe0','\xc2','\xe2','\xc4','\xe4','\xc3','\xe3','\xc5','\xe5','\xc6','\xe6','\xc7','\xe7','\xd0','\xf0','\xc9','\xe9','\xc8','\xe8','\xca','\xea','\xcb','\xeb','\xcd','\xed','\xcc','\xec','\xce','\xee','\xcf','\xef','\xd1','\xf1','\xd3','\xf3','\xd2','\xf2','\xd4','\xf4','\xd6','\xf6','\xd5','\xf5','\xd8','\xf8','\xdf','\xde','\xfe','\xda','\xfa','\xd9','\xf9','\xdb','\xfb','\xdc','\xfc','\xdd','\xfd','\xff','\xa9','\xae','\u2122','\u20ac','\xa2','\xa3','\u2018','\u2019','\u201c','\u201d','\xab','\xbb','\u2014','\u2013','\xb0','\xb1','\xbc','\xbd','\xbe','\xd7','\xf7','\u03b1','\u03b2','\u221e']
    filename = raw_input("Write the full name of the file you wish to fix: \n")
    filetext = open(filename,  'r')
    textcontent = filetext.read()
    newtext = ''
    for char in textcontent:
        if char not in funnychars:
            newtext = newtext + char
        else:
            newtext  = newtext + htmlcodes[funnychars.index(char)]
    resultfile = open('result.txt', 'w')
    resultfile.write(newtext)
    resultfile.close()
    filetext.close()


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


