import requests
import re
import feedparser

class PrepareService:

    def read_feed(self, rss_url):
      try:
        rss_feed = feedparser.parse(rss_url)
        return rss_feed
      except:
        return None

    def parse_rss_feed(self, rss_feed):
      parsed_feed = []
      
      for entry in rss_feed.entries:
        parsed_feed.append({
            'title': entry.title,
            'url': entry.link,
            'description': entry.description[:entry.description.find('.')],
            'summary': None,
            'sentiment': None,
            'topics': None,
            'video': False
        })

      return parsed_feed
      
    def get_only_text(self, url):
      page = urllib.request.urlopen(url).read().decode('utf8')
      soup = BeautifulSoup(page)
      text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
      return soup.title.text, text
       
    

