#!/usr/bin/python
#coding=utf-8

import urllib2
import re
#用来创建绝对路径
import urlparse


def download(url, num_retries=2, user_agent='wswp', proxy=None):
    print 'Downloading:',url
    headers = {'User-agent':user_agent}
    request = urllib2.Request(url, headers=headers)

    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500 <=e.code <600:
                #发生5xx错误时继续请求
                return download(url, num_retries-1)

    return html

#download('http://tieba.baidu.com/f?kw=%E5%85%89%E6%98%8E%E5%A4%A7%E9%99%86')

def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


def link_crawler(seed_url, link_regex):
    crawl_queue = [seed_url]
    #避免重复爬取相同链接
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        for link in get_links(html):
            if re.match(link_regex, link):
                link = urlparse.urljoin(seed_url, link)
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

#下载限速
class Throttle:
    def __init__(self,delay):
        self.delay = delay
        self.domains = {}

    def wait(self,url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)

        self.domains[domain] = datetime.datetime.now()

#每次下载之前调用
#throttle = Throttle(delay)
#...
#throttle.wait(url)
#result = download(url, headers, proxy=proxy, num_retries=num_retries)