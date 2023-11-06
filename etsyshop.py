import csv
import requests
from bs4 import BeautifulSoup
import re
import scrapy
from time import sleep

csv_col = ['url', 'shop_name', "sales_count","join_date", 'review_date', "twitter", "linkedin", "instagram", "facebook", "pinterest",
           "web_site", "email", "phone"]
csvfile = open('etsy_data.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_col)
writer.writeheader()
csvfile.flush()

filename = "etsy_urls_new.csv"
count = 0
with open(filename) as fp:
    line = csv.reader(fp, delimiter=",")
    for index, rows in enumerate(line):
        if index == 0 or not rows[0].strip():
            pass
        else:
            headers = {
                "authority": "www.etsy.com",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "sec-ch-ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
            }

            cookies = {
                "user_prefs": "XPC8aUZSaY_RqKVYG9N1YvVn4K9jZACCVPnrv2B0tFJosIuSTl5pTo6OUmqerruTko5SgDdUxAhC4SJiGQA.",
                "fve": "1696585722.0",
                "_fbp": "fb.1.1696585722995.7637238676556700",
                "ua": "531227642bc86f3b5fd7103a0c0b4fd6",
                "_gcl_au": "1.1.825527096.1696585737",
                "_ga": "GA1.1.471442667.1696585740",
                "lantern": "cd0480c6-389d-4595-adcb-80d8079c45d9",
                "_pin_unauth": "dWlkPVlqWXdaRFU0WlRjdE5USXlaQzAwTlRVd0xUa3hORGt0TnpkalptVXpZemhrT0RVNA",
                "cdn_exp_dd_rosey_2": "judy",
                "uaid": "oqyl-eDBCrW9s4tMEwvIN-JweitjZACCVPnrv8C0u9enaqXSxMwUJSslF5PyxLxCo9RyC8tAV9Oy3HRn3bDQco8gI9_ACqVaBgA.",
                "last_browse_page": "https%3A%2F%2Fwww.etsy.com%2Fshop%2FTheFive15",
                "_uetsid": "0170e8607bb111ee96b46575d491aece",
                "_uetvid": "93712060642d11eeabca97aab57a7d8f",
                "_ga_KR3J610VYM": "GS1.1.1699171065.2.1.1699172029.58.0.0",
                "datadome": "Mcv9Fv5r0wwLZNYvFxVycuuHSZH6MMGCk6ErI_xqEJqjaws9W87aHMc~7vamzU6yXhFhlM1KyM2pWi_hUCl1DGIPoz1p6YIJ3zVTqMrZMLCpSjg2d4PvZ9gcmQYdbcrD"
            }

            try:
                response = requests.get(rows[0], cookies=cookies, headers=headers)
            except KeyboardInterrupt:
                print("Exit")
            except Exception as e:
                print("Erro:", e, rows[0])
            if response.status_code == 404 or response.status_code ==403:
                item = dict()
                item['url'] = rows[0]
                writer.writerow(item)
                csvfile.flush()
                continue

            soup = BeautifulSoup(str(response.content), 'lxml')
            resp = scrapy.Selector(text=response.text)
            try:
                shop_name = soup.find('h1', {'class': 'wt-text-heading wt-text-truncate'}).text
            except:
                item = dict()
                item['url'] = rows[0]
                writer.writerow(item)
                csvfile.flush()
                continue

            about = soup.find('div', {'data-appears-component-name': 'shop_home_about_section'})
            if about:
                # print(about.get_text)
                about_info = about.find_all('span', class_='wt-text-title-largest wt-display-block')
                join_date = about_info[-1].get_text().strip()

                print("join_date", join_date)

            top_review = soup.find('div', class_='review-item')
            if top_review:
                review_date = \
                [v.strip() for v in resp.css("div.review-item")[0].css("p.shop2-review-attribution::text").getall() if
                 v.strip()][0].split("on")[-1].strip()

                print("review_date", review_date)

            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b|\b[A-Za-z0-9._%+-]+\s*(?:\[at\]|\[!at\]|AT|\(at\))\s*[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            email_list = []
            phone_pattern = r'\+\d{1,4} \d{3} \d{3} \d{4}|\b(?:\d{3} \d{3} \d{4}|\d{3}-\d{3}-\d{4}|)'
            phone_list = []

            social_medias = []
            web_sites = []
            if about:
                social_medias = about.find_all('a', class_='text-decoration-none')
                for social in set(social_medias):
                    print(social["aria-label"], social["href"])
                    if social["aria-label"] in ["shop-website"]:
                        web_sites.append(social["href"])

                email_list += re.findall(email_pattern, about.get_text())
                phone_list += re.findall(phone_pattern, about.get_text())

            announcement = soup.find('div', class_='announcement-section')
            if announcement:
                email_list += re.findall(email_pattern, announcement.get_text())
                phone_list += re.findall(phone_pattern, announcement.get_text())

            faq_div = soup.find('div', id='faq')
            if faq_div:
                email_list += re.findall(email_pattern, faq_div.get_text())
                phone_list += re.findall(phone_pattern, faq_div.get_text())

            top_announcement = soup.find('div', {'data-appears-component-name': "shop_home_announcement_section"})
            if top_announcement:
                email_list += re.findall(email_pattern, top_announcement.get_text())
                phone_list += re.findall(phone_pattern, top_announcement.get_text())

            phone_list = [''.join(caracter for caracter in s if caracter.isdigit() or caracter in [" ", "+", "-"]) for s
                          in phone_list if s.strip(".").strip() != ""]
            email_list = [s.strip() for s in email_list if s.strip() != ""]
            for i in set(map(str.strip, email_list)):
                print(i)

            for i in set(map(str.strip, phone_list)):
                print(i)

            item = dict()
            item['url'] = rows[0]
            item['shop_name'] = shop_name
            item['join_date'] = join_date
            item['review_date'] = review_date
            item['email'] = ";".join(list(set(email_list)))
            item['phone'] = ";".join(list(set(phone_list)))
            item['web_site'] = ";".join(list(set(web_sites)))
            for social in set(social_medias):
                if "twitter" in social["href"]:
                    item['twitter'] = social["href"]
                elif "facebook" in social["href"]:
                    item['facebook'] = social["href"]
                elif "linkedin" in social["href"]:
                    item['linkedin'] = social["href"]
                elif "instagram" in social["href"]:
                    item['instagram'] = social["href"]
                elif "pinterest" in social["href"]:
                    item['pinterest'] = social["href"]
            item['sales_count'] = "".join(resp.css("span.wt-text-caption.wt-no-wrap ::text").getall()).replace("Sales","").strip()
            writer.writerow(item)
            csvfile.flush()
            count += 1
            if count % 50 == 0:
                sleep(10)










