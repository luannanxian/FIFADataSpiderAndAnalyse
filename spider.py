# 运行前需要关闭clash代理，否则报错： requests.exceptions.ProxyError: HTTPSConnectionPool(host='sofifa.com', port=443): Max retries
# exceeded with url: / (Caused by ProxyError('Cannot connect to proxy.', OSError(0, 'Error')))

import gevent
from gevent import monkey

# monkey.patch_all()
import time
import requests
import random
from lxml import etree
import pandas as pd
from bs4 import BeautifulSoup

class FIFA21:

    def __init__(self):

        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.baseURL = 'https://sofifa.com/players?type=all&lg%5B%5D=13&lg%5B%5D=16&lg%5B%5D=19&lg%5B%5D=31&lg%5B%5D=53'  # 五大联赛球员
        # self.baseURL = 'https://sofifa.com/'  # 所有球员数据
        self.path = 'data.csv'
        self.row_num = 0
        self.title = ['player_name', 'basic_info', 'Overall_rating', 'Potential', 'Value', 'Wage',
                      'preferred_foot', 'weak_foot', 'skill_moves', 'international_reputation']
        self.small_file = ['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW', 'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM',
                           'RCM', 'RM', 'LWB',
                           'LDM', 'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB',
                           'RB', 'GK']
        self.details = ['Crossing', 'Finishing', 'Heading Accuracy', 'Short Passing', 'Volleys', 'Dribbling,Curve',
                        'FK Accuracy', 'Long Passing', 'Ball Control', 'Acceleration', 'Sprint Speed', 'Agility',
                        'Reactions',
                        'Balance', 'Shot Power', 'Jumping', 'Stamina', 'Strength', 'Long Shots', 'Aggression',
                        'Interceptions', 'Positioning',
                        'Vision', 'Penalties', 'Composure', 'Defensive' 'Awareness', 'Standing Tackle',
                        'Sliding Tackle', 'GK Diving',
                        'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes']
        for name in self.title:
            exec('self.' + name + '=[]')
        for name in self.small_file:
            exec('self.' + name + '=[]')
        for i in range(len(self.details)):
            exec('self.details_' + str(i) + '=[]')

    def loadPage(self, url):
        time.sleep(random.random())
        return requests.get(url, headers=self.headers)

    def get_player_links(self, url):
        print(self.baseURL[:-1])  # debug
        content = self.loadPage(url)
        content = BeautifulSoup(content.text, 'html.parser')
        part_player_urls=content.findAll('tr')
        for player_url in part_player_urls:

        html = etree.HTML(bytes(bytearray(content.text, encoding='utf-8')))
        player_links = html.xpath(
            "//div[@class='card']/table[@class='table table-hover persist-area']/tbody[@class='list']"
            "/tr/td[@class='col-name']/a[@role='tooltip']/@href")

        result = []
        for link in player_links:
            result.append(self.baseURL[:-77] + link)  # 如果是所有球员，就是-1；五大联赛就是-77

        return result
        # return [self.baseURL[:-1]+link for link in player_links]

    def next_page(self, url):

        content = self.loadPage(url)
        html = etree.HTML(content)
        new_page = html.xpath("//div[@class='pagination']/a/@href")
        if url == self.baseURL:
            return self.baseURL[:-77] + new_page[0]  # 如果是所有球员，就是-1；五大联赛就是-77
        else:
            if len(new_page) == 1:
                return 'stop'
            else:
                return self.baseURL[:-77] + new_page[1]  # 如果是所有球员，就是-1；五大联赛就是-77

    def Get_player_small_field(self, html):

        content = html.xpath(
            "//div[@class='center']/div[@class='grid']/div[@class='col col-4']/div[@class='card calculated']/div[@class='field-small']"
            "/div[@class='lineup']/div[@class='grid half-spacing']/div[@class='col col-2']/div/text()")
        content = content[1::2]

        length = len(content)
        for i in range(length):
            exec('self.' + self.small_file[i] + '.append(' + '\'' + content[i] + '\'' + ')')

        # return dict(zip(keys,values))

    def Get_player_basic_info(self, html):

        player_name = html.xpath("//div[@class='center']/div[@class='grid']/div[@class='col col-12']"
                                 "/div[@class='bp3-card player']/div[@class='info']/h1/text()")

        player_basic = html.xpath("//div[@class='center']/div[@class='grid']/div[@class='col col-12']"
                                  "/div[@class='bp3-card player']/div[@class='info']/div[@class='meta ellipsis']/text()")

        exec("self.player_name.append(" + "\"" + player_name[0] + "\"" + ")")
        exec('self.basic_info.append(' + '\'' + player_basic[-1] + '\'' + ')')

    def Get_rating_value_wage(self, html):

        overall_potential_rating = html.xpath("//div[2]/div[@class='grid']/div[@class='col col-12']"
                                              "/div[@class='bp3-card player']/section[@class='card spacing']/div[@class='block-quarter']/div/span[1]/text()")

        if len(overall_potential_rating) == 0:
            overall_potential_rating = html.xpath("//div[1]/div[@class='grid']/div[@class='col col-12']"
                                                  "/div[@class='bp3-card player']/section[@class='card spacing']/div[@class='block-quarter']/div/span[1]/text()")

        value_wage = html.xpath("//div[2]/div[@class='grid']/div[@class='col col-12']"
                                "/div[@class='bp3-card player']/section[@class='card spacing']/div[@class='block-quarter']/div/text()")

        if len(value_wage) == 0:
            value_wage = html.xpath("//div[1]/div[@class='grid']/div[@class='col col-12']"
                                    "/div[@class='bp3-card player']/section[@class='card spacing']/div[@class='block-quarter']/div/text()")

        exec('self.Overall_rating.append(' + '\'' + overall_potential_rating[0] + '\'' + ')')
        exec('self.Potential.append(' + '\'' + overall_potential_rating[1] + '\'' + ')')
        exec('self.Value.append(' + '\'' + value_wage[2] + '\'' + ')')
        exec('self.Wage.append(' + '\'' + value_wage[3] + '\'' + ')')

    # / html / body / div[1] / div / div[2] / div[1] / section / div[1] / div / span
    def Get_profile(self, html):

        profile = html.xpath(
            "//div[@class='center']/div[@class='grid']/div[@class='col col-12']/div[@class='block-quarter'][1]"
            "/div[@class='card']/ul[@class='pl']/li[@class='ellipsis']/text()[1]")

        exec('self.preferred_foot.append(' + '\'' + profile[0] + '\'' + ')')
        exec('self.weak_foot.append(' + '\'' + profile[1] + '\'' + ')')
        exec('self.skill_moves.append(' + '\'' + profile[2] + '\'' + ')')
        exec('self.international_reputation.append(' + '\'' + profile[3] + '\'' + ')')

    def Get_detail(self, html):

        # // *[ @ id = "body"] / div[3] / div / div[2] / div[9] / div / ul / li[1] / span[1]
        #  上面这一行， 在F12里面“复制XPath”就行了
        keys = html.xpath("//div[3]/div[@class='grid']/div[@class='col col-12']"
                          "/div[@class='block-quarter']/div[@class='card']/ul[@class='pl']/li/span[@role='tooltip']/text()")  # 为了防止能力值旁边有+-数值，span不能[2]，需要用@role制定字段

        if (len(keys) == 0):
            keys = html.xpath("//div[2]/div[@class='grid']/div[@class='col col-12']"
                              "/div[@class='block-quarter']/div[@class='card']/ul[@class='pl']/li/span[@role='tooltip']/text()")

        values = html.xpath("//div[3]/div[@class='grid']/div[@class='col col-12']"
                            "/div[@class='block-quarter']/div[@class='card']/ul[@class='pl']/li/span[1]/text()")
        if (len(values) == 0):
            values = html.xpath("//div[2]/div[@class='grid']/div[@class='col col-12']"
                                "/div[@class='block-quarter']/div[@class='card']/ul[@class='pl']/li/span[1]/text()")

        print(keys)  # debug
        print(values)  # debug

        values = values[:len(keys)]
        values = dict(zip(keys, values))

        for i in range(len(self.details)):
            if self.details[i] in keys:
                exec('self.details_' + str(i) + '.append(' + '\'' + values[self.details[i]] + '\'' + ')')
            else:
                exec('self.details_' + str(i) + '.append(' + '\'Nan\'' + ')')

        # return

    def start_player(self, url):

        content = self.loadPage(url)
        html = etree.HTML(content)

        # info= {}

        self.Get_player_basic_info(html)
        self.Get_profile(html)
        self.Get_rating_value_wage(html)
        self.Get_player_small_field(html)  # 各个位置评分
        self.Get_detail(html)
        self.row_num += 1

    def startWork(self):

        current_url = self.baseURL

        while (current_url != 'stop'):

            print(current_url)  # 首页，只有offset的区别
            player_links = self.get_player_links(current_url)  # 首页上所有球员的具体url，进入详情页
            # print(player_links)  # debug

            jobs = []
            for link in player_links:
                # self.start_player(link)
                # c = 1
                jobs.append(gevent.spawn(self.start_player, link))  # spawn创建协程任务，并加入到任务队列里
                # if c == 1:
                #     break
            # jobs = [gevent.spawn(self.start_player, link) for link in player_links]
            # 父线程阻塞，等待所有任务结束后继续执行
            gevent.joinall(jobs)

            current_url = self.next_page(current_url)

            # break

        self.save()
        # 循环get队列的数据，直到队列为空则退出

    def save(self):

        exec('df=pd.DataFrame()')
        for name in self.title:
            exec("df[" + "\'" + name + "\'" + "]=self." + name)
        for name in self.small_file:
            exec('df[' + '\"' + name + '\"' + ']=self.' + name)
        for i in range(len(self.details)):
            exec('df[' + '\"' + self.details[i] + '\"' + ']=self.details_' + str(i))

        exec('df.to_csv(self.path,index=False)')


if __name__ == "__main__":
    start = time.time()
    spider = FIFA21()
    spider.startWork()

    stop = time.time()
    print("\n[LOG]: %f seconds..." % (stop - start))
