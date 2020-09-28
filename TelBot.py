#!/usr/bin/env python
import telepot
from telepot.loop import MessageLoop 
import json
from os.path import expanduser
from os import getenv
import time

class TelBot(telepot.Bot):
    def __init__(self,token):


        proxyconf=getenv("http_proxy")
        proxyconf=open(expanduser('~/proxy'),'r').read().strip('\n')

        if proxyconf != None:
            proxy_user=proxyconf.split(":")[1].strip("//")
            proxy_pass=proxyconf.split(":")[2].split("@")[0]
            proxy_url="http://"+proxyconf.split("@")[1]
            telepot.api.set_proxy(proxy_url,(proxy_user,proxy_pass))

        telepot.Bot.__init__(self,token)
        # self.bot=telepot.Bot(token)
        # MessageLoop(self.bot,self.handle1)
        
    def posttry(self,msg,id):
        """ Enviar mensajes al grupo por el id """
       
        try:
            # self.sendMessage(id-1001334786762,msg,parse_mode="Markdown")
            print("Sent: "+msg)
        except:  
            print('Demasiados request. Esperando 5...')
            time.sleep(5)
            self.posttry(msg)

def handle1(msg):
    contenttype,chattype,chatid=telepot.glance(msg)
    print(contenttype,chattype,chatid)
    print(msg['text'])

if __name__ == "__main__":
    bot = TelBot("1314850663:AAFuBzMDs5niJiUXHvH6ZaWI9rXHaz7GX8A")
    print(bot.getMe())
    # print(bot.getUpdates())
    
    MessageLoop(bot,handle1).run_as_thread()
    # print("Listening")
    
    while 1:
        time.sleep(10)