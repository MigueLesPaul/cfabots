#!/usr/bin/env python
import os
from os.path import expanduser
import json
import time
from TelBot import TelBot
from FaceBot import Facebook
from TwittBot import TwitBot
import logging 
from systemd import journal

# Centro de Física de la Atmósfera 2020 
# Publicar salidas de SisPI en las redes sociales 
# Miguel 
# Ariel 
# Adrián 


log= logging.getLogger('CFABot')
log.addHandler(journal.JournaldLogHandler())
log.setLevel(logging.DEBUG)



class CFABot(TelBot,Facebook,TwitBot):
	""" 
	Publicar salidas de SisPI en las redes sociales
	Hereda de las clases especificas para cada una de las redes sociales utilizadas por rel CFA 
	"""
	def __init__(self):
		credentials = json.load(open(expanduser("~/credentials.json"),'r'))
		self.channel_id=credentials['Telegram channel_id']


		# super(TelBot, self  ).__init__(credentials['Telegram Bot Token'])
		TelBot.__init__(self,credentials['Telegram Bot Token'])

		# super(Facebook, self).__init__(p_page_id=credentials["Facebook Page Id"] ,p_page_access_token=credentials['Facebook Page Token'])
		Facebook.__init__(self,p_page_id=credentials["Facebook Page Id"] ,p_page_access_token=credentials['Facebook Page Token'])
		
		TwitBot.__init__(self)
		# super(TwitBot, self  ).__init__()



	def post_msg(self,msg):
		pass	
	def post_img(self,msg,imgfile):
		pass
	def post_vid(self,msg,vidfile):
		
		# Telegram
		try:
			response=self.sendVideo(self.channel_id,
                             video=open(vidfile, 'rb'),
                             width=480,
                             height=320,
                             caption=msg)
			print(response)
		except:
			msglog="Hubo un error al publicar en Telegram"
			log.info(msglog)
			log.exception("")
			print(msglog)

		# Twitter
		
		try:
			response = self.postUpdate(vidfile,msg)
			print(response)
		except:
			msglog="Hubo un error al publicar en Twitter"
			log.info(msglog)
			log.exception("")
			print(msglog)
		# Facebook	
		try:
			response=self.post_video(vidfile,msg)
			print(response)
		except:
			msglog="Hubo un error al publicar en Facebook"
			log.info(msglog)
			log.exception("")
			print(msglog)


# if __name__ == '__main__':
# 	bot = CFABot()	
# 	bot.post_vid('Post de prueba de bot Facebook','/home/miguel/Projects/cfabots/wrfout_2020082806_d3_rain_sfc_.mp4')	