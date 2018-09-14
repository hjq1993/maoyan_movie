# 以下是使用正则表达式方法提起猫眼电影top100的代码
import requests
import re
import json


def get_one_page():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)"
                             " AppleWebKit/537.36 (KHTML, like Gecko)"
                             " Chrome/67.0.3396.99 Safari/537.36"}
    url_list = "http://maoyan.com/board/4?offset={}"
    url = url_list.format(num)
    response = requests.get(url, headers=headers)
    html_str = response.content.decode()
    # print(response.content.decode()) # 打印输出的响应
    # 正则匹配信息，把需要的信息一一匹配出来
    results = re.findall('<dd>.*?board-index.*?>(.*?)</i>.*?title="(.*?)'
                         '".*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)'
                         '</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)'
                         '</i>.*?alt.*?class.*?src="(.*?)".*?</a>', html_str, re.S)
    #print(results)
    # 每匹配出一个条目的信息，其实是一个列表，列表包含的信息为元祖，对元祖取值，把值存到字典里即可
    for result in results:
        movie_dict = {}
        movie_dict["排名"] = result[0]
        movie_dict["电影名称"] = result[1]
        movie_dict["主演"] = result[2].replace("\n","").strip()
        movie_dict["上映时间"] = result[3]
        movie_dict["评分"] = result[4]+result[5]
        movie_dict["图片"] = result[6]
        #print(result)
        print(movie_dict)
        # 写入到文本文件
        with open("mydy_zhengze.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(movie_dict, ensure_ascii=False))
            f.write("\n")


if __name__ == '__main__':
    # 从每一页开始爬取，到最后一页。根据观察，url变化为offset后面参数从0开始，每一个加10
    num = 0
    while num <= 100:
        get_one_page()
        num += 10


