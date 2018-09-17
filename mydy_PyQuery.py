# 以下是使用正则表达式方法提起猫眼电影top100的代码
import requests
from pyquery import PyQuery as pq
import json


class MaoMovie:
    def __init__(self):
        self.url = "http://maoyan.com/board/4?offset={}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)"
                                      " AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/67.0.3396.99 Safari/537.36"}

    # 获取响应
    def parse(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_shuju(self,html_str):
        doc = pq(html_str)
        movie_list = doc("dd").items()
        for list in movie_list:
            paiming = list.find(".board-index").text()
            movie = list.find(".name").text()
            star = list.find(".star").text()
            time = list.find(".releasetime").text()
            score = list.find(".integer").text() + list.find(".fraction").text()
            picture = list.find(".board-img").attr("data-src")
            # print(picture)
            # 图片获取，如果代码写成li.find(".board-img").attr("data-src")，则获取不到
            # element显示的代码和network实际的代码不一样，可能经过渲染，导致代码发生了变化
            # 需要以network里的代码去获取信息
            movie_dict = {}
            movie_dict["排名"] = paiming
            movie_dict["电影名称"] = movie
            movie_dict["主演"] = star
            movie_dict["上映时间"] = time
            movie_dict["得分"] = score
            movie_dict["图片"] = picture
            # print(movie_dict)
            with open("mydy_PyQuery.txt", "a", encoding="utf-8") as f:
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
    maoyan = MaoMovie()
    maoyan.run()