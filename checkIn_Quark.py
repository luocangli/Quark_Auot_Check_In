import os 
import re 
import sys 
import requests
import json

cookie_list = os.getenv("COOKIE_QUARK").split('\n|&&')

# 替代 notify 功能
def send(title, message):
    send_message = f"{title}: {message}"
    print(send_message)
    send_dingtalk_message(send_message)
    send_wxpusher_message(send_message)

# 获取环境变量 
def get_env(): 
    # 判断 COOKIE_QUARK是否存在于环境变量 
    if "COOKIE_QUARK" in os.environ: 
        # 读取系统变量以 \n 或 && 分割变量 
        cookie_list = re.split('\n|&&', os.environ.get('COOKIE_QUARK')) 
    else: 
        # 标准日志输出 
        print('❌未添加COOKIE_QUARK变量') 
        send('夸克自动签到', '❌未添加COOKIE_QUARK变量') 
        # 脚本退出 
        sys.exit(0) 

    return cookie_list 

# 推送钉钉群机器人消息
def send_dingtalk_message(message):
    headers = {
        'Content-Type': 'application/json',
    }
    
    payload = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }

    # 判断 DINGTALK_WEBHOOK 是否存在于环境变量 
    if "DINGTALK_WEBHOOK" in os.environ: 
        webhook_url = os.environ.get('DINGTALK_WEBHOOK')
    else: 
        # 标准日志输出 
        print('❌ 未添加DINGTALK_WEBHOOK变量') 
        return
    
    if webhook_url is None:
        print("❌ DINGTALK_WEBHOOK变量不存在. 请检查你的配置")
        return
    
    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        print("✅ 钉钉推送消息发送成功")
    else:
        print(f"❌ 钉钉推送消息发送失败, 状态码: {response.status_code}, 响应内容: {response.json()}")

## 推送WxPusher消息
def send_wxpusher_message(message):
    url = "https://wxpusher.zjiecode.com/api/send/message"
    headers = {"Content-Type": "application/json"}

    # 判断 WX_PUSHER_APP_TOKEN 是否存在于环境变量 
    if "WX_PUSHER_APP_TOKEN" in os.environ: 
        app_token = os.environ.get('WX_PUSHER_APP_TOKEN')
    else: 
        # 标准日志输出 
        print('❌ 未添加WX_PUSHER_APP_TOKEN变量') 
        return
    
    if app_token is None:
        print("❌ WX_PUSHER_APP_TOKEN变量不存在. 请检查你的配置")
        return

    # 判断 WX_PUSHER_UID 是否存在于环境变量 
    if "WX_PUSHER_UID" in os.environ: 
        uid = os.environ.get('WX_PUSHER_UID')
    else: 
        # 标准日志输出 
        print('❌ 未添加WX_PUSHER_UID变量') 
        return
    
    if uid is None:
        print("❌ WX_PUSHER_UID变量不存在. 请检查你的配置")
        return

    data = {
        "appToken": app_token,
        "content": message,
        "summary": "夸克网盘自动签到任务",  # 消息摘要
        "contentType": 1,  # 1 表示文字消息
        "uids": [uid],  # 接收消息的用户 UID
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("✅ WxPusher推送消息发送成功")
    else:
        print(f"❌ WxPusher推送消息发送失败, 状态码: {response.status_code}, 响应内容: {response.json()}")

# 其他代码...
class Quark:
    '''
    Quark类封装了签到、领取签到奖励的方法
    '''
    def __init__(self, user_data):
        '''
        初始化方法
        :param user_data: 用户信息，用于后续的请求
        '''
        self.param = user_data

    def convert_bytes(self, b):
        '''
        将字节转换为 MB GB TB
        :param b: 字节数
        :return: 返回 MB GB TB
        '''
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = 0
        while b >= 1024 and i < len(units) - 1:
            b /= 1024
            i += 1
        return f"{b:.2f} {units[i]}"

    def get_growth_info(self):
        '''
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        '''
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        response = requests.get(url=url, params=querystring).json()
        #print(response)
        if response.get("data"):
            return response["data"]
        else:
            return False

    def get_growth_sign(self):
        '''
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        '''
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        data = {"sign_cyclic": True}
        response = requests.post(url=url, json=data, params=querystring).json()
        #print(response)
        if response.get("data"):
            return True, response["data"]["sign_daily_reward"]
        else:
            return False, response["message"]

    def queryBalance(self):
        '''
        查询抽奖余额
        '''
        url = "https://coral2.quark.cn/currency/v1/queryBalance"
        querystring = {
            "moduleCode": "1f3563d38896438db994f118d4ff53cb",
            "kps": self.param.get('kps'),
        }
        response = requests.get(url=url, params=querystring).json()
        # print(response)
        if response.get("data"):
            return response["data"]["balance"]
        else:
            return response["msg"]

    def do_sign(self):
        '''
        执行签到任务
        :return: 返回一个字符串，包含签到结果
        '''
        log = ""
        # 每日领空间
        growth_info = self.get_growth_info()
        if growth_info:
            log += (
                f" {'88VIP' if growth_info['88VIP'] else '普通用户'} {self.param.get('user')}\n"
                f"💾 网盘总容量：{self.convert_bytes(growth_info['total_capacity'])}，"
                f"签到累计容量：")
            if "sign_reward" in growth_info['cap_composition']:
                log += f"{self.convert_bytes(growth_info['cap_composition']['sign_reward'])}\n"
            else:
                log += "0 MB\n"
            if growth_info["cap_sign"]["sign_daily"]:
                log += (
                    f"✅ 签到日志: 今日已签到+{self.convert_bytes(growth_info['cap_sign']['sign_daily_reward'])}，"
                    f"连签进度({growth_info['cap_sign']['sign_progress']}/{growth_info['cap_sign']['sign_target']})\n"
                )
            else:
                sign, sign_return = self.get_growth_sign()
                if sign:
                    log += (
                        f"✅ 执行签到: 今日签到+{self.convert_bytes(sign_return)}，"
                        f"连签进度({growth_info['cap_sign']['sign_progress'] + 1}/{growth_info['cap_sign']['sign_target']})\n"
                    )
                else:
                    log += f"❌ 签到异常: {sign_return}\n"
        else:
            log += f"❌ 签到异常: 获取成长信息失败\n"

        return log


def main():
    '''
    主函数
    :return: 返回一个字符串，包含签到结果
    '''
    msg = ""
    global cookie_quark
    cookie_quark = get_env()

    print("✅ 检测到共", len(cookie_quark), "个夸克账号\n")

    i = 0
    while i < len(cookie_quark):
        # 获取user_data参数
        user_data = {}  # 用户信息
        for a in cookie_quark[i].replace(" ", "").split(';'):
            if not a == '':
                user_data.update({a[0:a.index('=')]: a[a.index('=') + 1:]})
        # print(user_data)
        # 开始任务
        log = f"🙍🏻‍♂️ 第{i + 1}个账号"
        msg += log
        # 登录
        log = Quark(user_data).do_sign()
        msg += log + "\n"

        i += 1

    # print(msg)

    try:
        send('夸克自动签到', msg)
    except Exception as err:
        print('%s\n❌ 错误，请查看运行日志！' % err)

    return msg[:-1]


if __name__ == "__main__":
    print("----------夸克网盘开始签到----------")
    main()
    print("----------夸克网盘签到完毕----------")
