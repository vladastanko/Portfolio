from bs4 import BeautifulSoup
import requests
import time
import datetime
import smtplib
import csv


URL = 'https://www.amazon.com/dp/B00WYT6FPE/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B00WYT6FPE&pd_rd_w=8Quc7&content-id=amzn1.sym.eb7c1ac5-7c51-4df5-ba34-ca810f1f119a&pf_rd_p=eb7c1ac5-7c51-4df5-ba34-ca810f1f119a&pf_rd_r=KWXTA0YQX1ZZMNK87FHZ&pd_rd_wg=bAKBN&pd_rd_r=5a74573b-e35e-438f-ad50-db3cd7f185bc&s=apparel&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

page = requests.get(URL, headers=headers)
soup1 = BeautifulSoup(page.content, "html.parser")
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

title = soup2.find(id="productTitle").get_text()
title = title.strip()
price = soup2.find(id="corePriceDisplay_desktop_feature_div").get_text()
price = price.strip()[1:6]
today = datetime.date.today()


header = ["Title", "Price", "Date"]
data = [title, price, today]

with open("AmazonDataset.csv", "w", newline="", encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)


# appending data

with open("AmazonDataset.csv", "a+", newline="", encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerow(data)


def check_price():
    URL = 'https://www.amazon.com/dp/B00WYT6FPE/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B00WYT6FPE&pd_rd_w=8Quc7&content-id=amzn1.sym.eb7c1ac5-7c51-4df5-ba34-ca810f1f119a&pf_rd_p=eb7c1ac5-7c51-4df5-ba34-ca810f1f119a&pf_rd_r=KWXTA0YQX1ZZMNK87FHZ&pd_rd_wg=bAKBN&pd_rd_r=5a74573b-e35e-438f-ad50-db3cd7f185bc&s=apparel&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id="productTitle").get_text()
    title = title.strip()
    price = soup2.find(id="corePriceDisplay_desktop_feature_div").get_text()
    price = price.strip()[1:6]
    today = datetime.date.today()

    header = ["Title", "Price", "Date"]
    data = [title, price, today]

    with open("AmazonDataset.csv", "a+", newline="", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(data)

while(True):
    check_price()
    time.sleep(86400)