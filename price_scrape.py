import time
import requests
import sqlite3
import logging
import smtplib
import getpass
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

class PriceDB(object):
    def __init__(self, file_name, recreate = False):
        self.db_name = file_name
        self.price_hist_table = "price_history"
        self.conn = sqlite3.connect(self.db_name)
        cur = self.conn.cursor()
        if recreate:
            logging.info("Dropping table")
            cur.execute('drop table if exists ' + self.price_hist_table)
            result = None
            self.conn.commit()
        else:
            cur.execute("select * from sqlite_master where type='table' and name='{0}'".format(self.price_hist_table))
            result = cur.fetchone()
        if not result:
            logging.info("Creating table")
            cur.execute("create table {0} (url text, ts_begin integer, ts_end integer, reg_price real, discount_price real, PRIMARY KEY (url, ts_begin))".format(self.price_hist_table))
            self.conn.commit()
        #cols = [d[0] for d in cur.description]

    def updatePrice(self,  url, reg_price, discount_price):
        cur = self.conn.cursor()
        cur.execute("select max(ts_begin), reg_price, discount_price from {0} where url='{1}'".format(self.price_hist_table, url))
        result = cur.fetchone()
        new_ts = int(time.time()*1000) # in milliseconds
        if result and reg_price == result[1] and discount_price == result[2]:
            # No change, just update end time
            cur.execute("update {0} set ts_end={1} where url='{2}' and ts_begin={3}".format(self.price_hist_table, new_ts, url, result[0]))
        else:
            cur.execute("insert into {0}(url, ts_begin, ts_end, reg_price, discount_price) values ('{1}', {2}, {2}, {3}, {4})"
                        .format(self.price_hist_table, url, new_ts, reg_price, discount_price))
        self.conn.commit()

def priceToFloat(str):
    str = str.strip("$")
    try:
        price = float("".join(str.split(",")))
    except ValueError, e:
        logging.warn("Unable to parse price '"  + str + "'")
        price = None
    return price

def getPrices(url):
    try:
        url_response = requests.get(url)
        if url_response.status_code != 200:
            logging.warn("Bad response code:" + str(url_response.status_code))
            return None, None
    except requests.exceptions.RequestException, e:
        logging.warn("Connection error: " + e.message)
        return None, None
    #html_text = url_response.text.encode('ascii', 'ignore')
    html_text = url_response.text
    soup = BeautifulSoup(html_text, "html.parser")
    prices = soup.find("div", {"id": "PriceDisplay"})
    if prices:
        reg_price = prices.find("span", {"class": "priceBig"})
        net_price = prices.find("input", {"class": "netPrice"})
        if reg_price and net_price:
            return (priceToFloat(reg_price.text), priceToFloat(net_price["value"]))
    return None, None

def sendMail(subject, msg_body, passwd):
    msg = MIMEText(msg_body)
    sender = "rainzforever@hotmail.com"
    receivers = ["yuzhao30@yahoo.com"]
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers
    logging.info("Sending email: " + msg_body)
    try:
        s = smtplib.SMTP('smtp.live.com', 587)
        s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(sender, passwd)
        s.sendmail(sender, receivers, msg.as_string())
        s.quit()
    except Exception as e:
        logging.exception("Failed to send email")

    
    
def main():
    logging.basicConfig(filename='scrape.log', level=logging.WARNING)
    logging.info("Started.")
    passwd = getpass.getpass()
    db = PriceDB("prices.db")
    url_list = [
        "http://www1.bloomingdales.com/shop/product/canada-goose-kensington-parka?ID=1068582&CategoryID=1004024",
        "http://www1.bloomingdales.com/shop/product/canada-goose-trillium-parka?ID=1068587&CategoryID=1004024",
        "http://www1.bloomingdales.com/shop/product/canada-goose-langford-parka-with-fur-hood?ID=769781&CategoryID=1004024",
        "http://www1.bloomingdales.com/shop/product/canada-goose-citadel-parka-with-fur-hood?ID=1081639&CategoryID=1004024",
        "http://www1.bloomingdales.com/shop/product/salvatore-ferragamo-ballet-flats-varina?ID=1066212&CategoryID=16961",
        "http://www1.bloomingdales.com/shop/product/salvatore-ferragamo-crossbody-ginny?ID=1167805&CategoryID=19209",
    ]
    running = True
    while running:
        for url in url_list:
            reg_price, net_price = getPrices(url)
            if reg_price is None or net_price is None:
                continue # ERROR: unable to get price
            if net_price:
                discount = (reg_price - net_price) / float(reg_price)
            else:
                discount = "N/A"
            print url, reg_price, net_price, discount
            db.updatePrice(url, reg_price, net_price)
            if discount >= 0.5:
                msg_body = "{0}: {1}% discount".format(url, discount*100)
                sendMail("Discount Alert", msg_body, passwd)
        time.sleep(30)
main()
