from gtts import gTTS
import os
import json
from urllib.request import urlopen,Request
from urllib.error import URLError
from urllib.parse import urlencode
from wxpy import *
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


class TuringChatMode(object):
    """this mode base on turing robot"""

    def __init__(self):
        # API接口地址
        self.turing_url = 'http://www.tuling123.com/openapi/api?'

    def get_turing_text(self,text):
        ''' 请求方式:   HTTP POST
            请求参数:   参数      是否必须        长度          说明
                        key        必须          32           APIkey
                        info       必须          1-32         请求内容，编码方式为"utf-8"
                        userid     必须          32           MAC地址或ID
        '''
        turing_url_data = dict(
            key = '6b8d0fae75a64ecb81aeed6695831d74',
            info = text,
            userid = '101270',

        )
        # print("The things to Request is:",self.turing_url + urlencode(turing_url_data))
        self.request = Request(self.turing_url + urlencode(turing_url_data))
        # print("The result of Request is:",self.request)

        try:
            w_data = urlopen(self.request)
            # print("Type of the data from urlopen:",type(w_data))
            # print("The data from urlopen is:",w_data)
        except URLError:
            raise IndexError("No internet connection available to transfer txt data")
            # 如果发生网络错误，断言提示没有可用的网络连接来传输文本信息
        except:
            raise KeyError("Server wouldn't respond (invalid key or quota has been maxed out)")
            # 其他情况断言提示服务相应次数已经达到上限

        response_text = w_data.read().decode('utf-8')
        # print("Type of the response_text :",type(response_text))
        # print("response_text :",response_text)

        json_result = json.loads(response_text)
        # print("Type of the json_result :",type(json_result))
        return json_result['text']

chatbot = ChatBot("zxh")# 用于回复消息的机器人
# chatbot.set_trainer(ChatterBotCorpusTrainer)
# chatbot.train("chatterbot.corpus.chinese")# 使用该库的中文语料库

bot = Bot(cache_path=True)# 用于接入微信的机器人
group_2 = bot.friends().search('forex')[0]# 进行测试的群
#group_2 = bot.friends.search("刘文华")[0]
group_2.send("hello")
turing = TuringChatMode()

@bot.register(group_2)
def reply_my_friend(msg):
   print(msg)
   turing_data = turing.get_turing_text(msg)
   print("Robot:", turing_data)
   tts = gTTS(text=turing_data, lang='zh-tw')
  # replay = chatbot.get_response(turing_data).text
   group_2.send(turing_data)
   tts.save("hello2.mp3")
   group_2.send_image('a.jpg')
   group_2.send_file('hello2.mp3')
   return chatbot.get_response(turing_data).text# 使用机器人进行自动回复

# @bot.register(group_2)
# def reply_image(msg):
#     print(msg)
#     group_2.send_image('a.jpg')
# 堵塞线程，并进入 Python 命令行
embed()