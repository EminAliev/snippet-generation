import requests
import re

class RSSParser:

    def __init__(self):
        self.items_regex = re.compile('<item.*?>(.*?)<\/item>', re.S)
        self.details_title_regex = re.compile('<title.*?>(.*?)<\/title>', re.S)
        self.details_link_regex  = re.compile('<link.*?>(.*?)<\/link>', re.S)
        self.details_date_regex  = re.compile('<pubDate>(.*?)<\/pubDate>', re.S)
     
    def parse(self, url):
        items = []
        response = requests.get(url).text
        tmpItems = self.items_regex.findall(response)
        for i in tmpItems:
          items.append({"title": self.details_title_regex.search(i).group(1), "link": self.details_link_regex.search(i).group(1), "date": self.details_date_regex.search(i).group(1)})
        return items

if __name__ == "__main__":
  print(RSSParser().parse(url ='https://media.kpfu.ru/news-rss'))
