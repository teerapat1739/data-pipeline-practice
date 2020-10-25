from bs4 import BeautifulSoup
import requests
import http.client
import mimetypes
from configuration import GetConfiguration
from broker.publish import rabbit_publish


cfg = GetConfiguration()
send_api = rabbit_publish()
routing_key = cfg["rabbit_database"]["routing_key"]

if __name__ == "__main__":
    conn = http.client.HTTPSConnection("www.posttoday.com")
    payload = ''
    headers = {}
    all_path = ["/rss/src/politics.xml", "/rss/src/world.xml", "/rss/src/economy.xml", "/rss/src/money.xml"]
    dict_item = {"title": "","date":"","url":"","source":""}  
    for i in range(len(all_path)):
        conn.request("GET", all_path[i], payload, headers)
        res = conn.getresponse()
        data = res.read()
        soup = BeautifulSoup(data.decode("utf-8"), 'lxml')
        items = soup.find_all('item')
        for item in items:
            try:
                dict_item["title"] = item.get_text('split').split('split')[0]
                dict_item["date"] = " ".join(item.get_text('split').split('split')[3].split(' ')[1:4])
                dict_item["url"] = item.get_text('split').split('split')[1]
                dict_item["source"] = "posttoday"
                print("-----",dict_item)
                send_api.send(dict_item, routing_key)
            except:
                dict_item["title"] = item.get_text('split').split('split')[0]
                dict_item["date"] = " ".join(item.get_text('split').split('split')[2].split(' ')[1:4])
                dict_item["url"] = item.get_text('split').split('split')[1]
                dict_item["source"] = "posttoday"
                # send_api.send(dict_item,routing_key)