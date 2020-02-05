import time
from weibo import Weibo
from apscheduler.schedulers.blocking import BlockingScheduler
from setting import getWeiboConfig
from reporter import send

# 实例化 BlockingScheduler
sched = BlockingScheduler()

# 声明两个全局变量保存所有监控对象的状态和ID
global weibo_id_dict
global first_check_dict

weibo_id_dict = {}
first_check_dict = {}

# 查询时间间隔初始化
interval_wb = 300


def getWeibo(i):
    contrainerID = i["contrainerID"]
    weibo = Weibo(contrainerID)
    weiboID = i["weiboID"]
    print(f"正在扫描 {weiboID}")
    try:
        # 初次启动记录前十条微博id
        if first_check_dict[contrainerID] is True:
            weibo_id_array = weibo.IdArray
            weibo_id_dict[contrainerID] = weibo_id_array
            first_check_dict[contrainerID] = False

        if first_check_dict[contrainerID] is False:
            # 取最新的前三条微博
            for idcount in range(0, 3):
                # 广告位微博id为0，忽略
                if int(weibo.IdArray[idcount]) == 0:
                    continue
                # 微博id不在记录的id列表里，判断为新微博
                if weibo.IdArray[idcount] not in weibo_id_dict[contrainerID]:
                    # 将id计入id列表
                    weibo_id_dict[contrainerID].append(weibo.IdArray[idcount])

                    # 检查新微博是否是转发
                    if weibo.checkRetweet(idcount):
                        print("IGNORE REPOST TEXT")
                    else:
                        text = weibo.getWeibo(idcount)
                        url = weibo.getScheme(idcount)

                        tag = True

                        for word in i['keyword']:
                            if word not in text:
                                tag = False

                        if tag is True:
                            print("FIND NEW MESSAGE")
                            if i['shieldingWords'] == "":
                                title = f"{weiboID} 微博更新提醒"
                                mail_msg = text + "\n" + url
                                send(mail_msg, title)

                            if i['shieldingWords'] != "" and i['shieldingWords'] not in text:
                                title = f"{weiboID} 微博更新提醒"
                                mail_msg = text + "\n" + url
                                send(mail_msg, title)
                            else:
                                print("FIND SHIELDINGWORDS,")

                        else:
                            print("TEXT DON'T MATCH")

                    time.sleep(0.5)

                else:
                    pass

    except Exception as e:
        print('ERROR WHEN GET WEIBO', e)
    finally:
        pass


def main():
    tasks = getWeiboConfig()

    for i in tasks:
        contrainerID = i["contrainerID"]
        weibo_id_dict[contrainerID] = []
        first_check_dict[contrainerID] = True
        sched.add_job(func=getWeibo, args=[i], trigger='interval', seconds=interval_wb, coalesce=True,
                      max_instances=5)
    sched.start()


if __name__ == '__main__':
    main()
