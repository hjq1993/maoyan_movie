# 以下是使用xpath方法提起猫眼电影top100的代码

import requests
import json
from lxml import etree


class MaoYan:
    def __init__(self):
        self.url = "http://maoyan.com/board/4?offset={}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)" \
                                     " AppleWebKit/537.36 (KHTML, like Gecko)" \
                                     " Chrome/67.0.3396.99 Safari/537.36"}

    def parse(self, url):
        response = requests.get(url,headers=self.headers)
        return response.content.decode()

    def get_shuju(self, html_str):
        element = etree.HTML(html_str)
        ret1 = element.xpath("//dl/dd")
        # print(ret1)
        with open("mydy_xpath.txt", "a", encoding="utf-8") as f:
            for concent in ret1:
                movie_dict = {}
                movie_dict["排名"] = concent.xpath("./i/text()")[0]
                movie_dict["电影名称"] = concent.xpath(".//p/a/text()")[0]
                # movie_dict["图片"] = concent.xpath("./a/img[@class='board-img']/@src")
                movie_dict["主演"] = concent.xpath(".//p[@class='star']/text()")[0].replace("\n", "").strip()
                movie_dict["上映时间"] = concent.xpath(".//p[@class='releasetime']/text()")[0][5:]
                movie_dict["评分"] = concent.xpath(".//i[@class='integer']/text()")[0] + concent.xpath(".//i[@class='fraction']/text()")[0]
                print(movie_dict)
                f.write(json.dumps(movie_dict, ensure_ascii=False))
                f.write("\n")

    def run(self):
        num = 0
        # 从第一页开始爬取，到第10页，每页的url规律为offset变化从是10
        while num < 100:
            url = self.url.format(num)
            html_str = self.parse(url)
            self.get_shuju(html_str)
            num += 10


if __name__ == '__main__':
    maoyan = MaoYan()
    maoyan.run()