import os
import json
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import configparser


# -----------------------读取微博配置文件--------------------------------

def getWeiboConfig():
    with open("weibo.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


# -----------------------读取邮箱配置文件--------------------------------

def mailConfig():
    mail_conf = {}
    cf = configparser.ConfigParser()
    cf.read("mail.conf")
    mail_conf["mail_host"] = cf.get("email", "mail_host")
    mail_conf["mail_user"] = cf.get("email", "mail_user")
    mail_conf["mail_pass"] = cf.get("email", "mail_pass")
    mail_conf["receivers"] = cf.get("email", "receivers").split(",")
    return mail_conf


mailConfig()


# -----------------------转换成短链接--------------------------------
def get_short_url(long_url_str):
    try:
        url = 'http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=' + str(long_url_str)
        response = requests.get(
            url,
            verify=False,
            timeout=5
        ).json()
        urlShort = response[0]['url_short']
        return urlShort
    except Exception as e:
        return str(long_url_str)
