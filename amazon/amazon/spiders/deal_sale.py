import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from time import sleep
# import json
# from urllib.parse import urljoin
# import re


class DealSaleSpider(scrapy.Spider):
    name = "deal_sale"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/s?k=iphone&crid=2TAYFGCPFYFMZ&sprefix=iphone%2Caps%2C228&ref=nb_sb_ss_ts-doa-p_2_6"]
    
    headers = {
        "Accept-Ch": "ect,rtt,downlink,device-memory,sec-ch-device-memory,viewport-width,sec-ch-viewport-width,dpr,sec-ch-dpr,sec-ch-ua-platform,sec-ch-ua-platform-version",
        "Accept-Ch-Lifetime": "86400",
        "Alt-Svc": "h3=':443'; ma=86400",
        "Cache-Control": "no-cache",
        "Cache-Control": "no-transform",
        "Content-Encoding": "gzip",
        "Content-Language": "en-IN",
        "Content-Security-Policy": "upgrade-insecure-requests;report-uri https://metrics.media-amazon.com/",
        "Content-Security-Policy-Report-Only": "default-src 'self' blob: https: data: mediastream: 'unsafe-eval' 'unsafe-inline';report-uri https://metrics.media-amazon.com/",
        "Content-Type": "text/html;charset=UTF-8",
        "Date": "Fri, 29 Mar 2024 09:49:20 GMT",
        "Expires": "-1",
        "Pragma": "no-cache",
        "Server": "Server",
        "Strict-Transport-Security": "max-age=47474747; includeSubDomains; preload",
        "Vary": "Content-Type,Accept-Encoding,User-Agent",
        "Via": "1.1 a16162a6669bc032095213406705ae78.cloudfront.net (CloudFront)",
        "X-Amz-Cf-Id": "k-pcv-0jn89z50sqAhZFFqqUsLtGfffSBx7h2fKBW-wiEwCquzI9uA==",
        "X-Amz-Cf-Pop": "BOM78-P2",
        "X-Amz-Rid": "3PCH8JY451VK36A71H2B",
        "X-Cache": "Miss from cloudfront",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-Xss-Protection": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"
    }
    
    rules = (Rule(LinkExtractor(allow="")),)

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': headers
    }
    
            
    def parse(self, response):   
        for links in response.xpath("//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']"):
                urlss = links.xpath("@href").get()
                ab_urls = response.urljoin(urlss)
                yield response.follow(url=ab_urls,callback=self.product_data)
                
        for nxt in range(1,20):
            page = response.xpath("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator']/@href").get()
            ab_page = response.urljoin(page)
            yield response.follow(url=ab_page,callback=self.parse)
            
            for link in response.xpath("//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']"):
                urls = link.xpath("@href").get()
                ab_url = response.urljoin(urls)
                yield response.follow(url=ab_url,callback=self.product_data)
            
            
            
    def product_data(self, response):
        yield{
            "Name": response.xpath("//span[@id='productTitle']/text()").get(),
            "Price": response.xpath("(//span[@class='a-price-whole']/text())[4]").get()
        }
        