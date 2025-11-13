import random
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

USER_AGENTS = [
    # Add more real user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0'
]

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agents):
        self.user_agents = random.choice(USER_AGENTS)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agents=crawler.settings.get('USER_AGENTS_LIST'))
    
    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.user_agents
