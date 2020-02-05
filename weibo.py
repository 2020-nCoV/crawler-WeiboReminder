import setting
import requests
import re


class Weibo():
    response = {}
    IdArray = []

    def __init__(self, contranerID):
        self.contranerID = contranerID
        super(Weibo, self).__init__()

        url = "https://m.weibo.cn/api/container/getIndex?containerid=" + str(contranerID)

        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 \
            Safari/537.36'}
        form = {
            'containerid': int(contranerID),
        }
        # 设置response
        self.response = requests.post(url, form, headers=header, timeout=20).json()
        # 设置id序列
        self.IdArray = self.getIdArray()

    # 去除html标签
    def dr_to_dd(self, dr_str):
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', dr_str)
        return str(dd)

    # 获取id序列
    def getIdArray(self):
        weibo_id_array = []
        cards = self.response['data']['cards']
        for card in cards:
            try:
                weibo_id = card['mblog']['id']
            except Exception as e:
                # 广告位无id，将其置0
                weibo_id_array.append("0")
            else:
                weibo_id_array.append(weibo_id)

        return weibo_id_array

    # 检查id
    def checkId(self, i):
        datas = self.response['data']['cards'][i]
        return str(datas['mblog']['id'])

    # 检查是否为转发微博
    def checkRetweet(self, i):
        datas = self.response['data']['cards'][i]
        if datas['mblog'].get('retweeted_status') is None:
            return False
        else:
            return True

    # 获取微博正文
    def getWeibo(self, i):
        datas = self.response['data']['cards'][i]
        r_weibo = str(datas['mblog']['text'])
        r2d_weibo = self.dr_to_dd(r_weibo)
        return r2d_weibo

    # 获取微博链接
    def getScheme(self, i):
        datas = self.response['data']['cards'][i]
        # 转换为短网址
        url = setting.get_short_url(str(datas['scheme']))
        return str(url)
