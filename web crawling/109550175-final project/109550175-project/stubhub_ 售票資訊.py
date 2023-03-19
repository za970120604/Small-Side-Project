from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import json 

def ticket_info(query_name):
    url="https://www.stubhub.tw/search/index?q="+query_name
    response=requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    page_to_scrape=[]
    page_to_scrape=re.findall("<a href=\"https:\/\/www\.stubhub\.tw\/.*\/ca.*\n.*<span class=\"tit-evento\">",soup.prettify())[0].split("\n")

    url1=page_to_scrape[0].replace("<a href=\"","")
    url1=url1.replace("\">","")
    response1=requests.get(url1)
    soup1 = BeautifulSoup(response1.text, "html.parser")

    res=re.findall("<script type=\"application\/ld\+json\">(.*?)<\/script>",str(soup1),flags=re.DOTALL)

    for item in res:
        item=item.replace("\n","")
        item1=json.loads(item)
        print("活動名稱:",item1["name"])
        try:
            print("舉辦地點:",item1["location"]["address"]["addressCountry"],item1["location"]["address"]["addressLocality"],"---",item1["location"]["name"])
        except KeyError:
            print("The place to hold the concert has not been chosen!!")
        try:
            print("日期:",item1["startDate"])
        except KeyError:
            print("The concert's date has not been chosen!!")
        try:
            print("價格: 自",item1["offers"]['price'],end=" ")
            print(item1["offers"]["priceCurrency"],"起")
        except KeyError:
            print("The ticket's price has not been decided!!")
        print("購票網址:",item1["url"])
        print("==========================================================================")





