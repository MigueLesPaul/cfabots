import os
from os.path import expanduser
import json
import time
import twitter


class  TwitBot(object):
	"""docstring for  TwitBot"""
	def __init__(self):
		super( TwitBot, self).__init__()
		
		credentials = json.load(open(expanduser("~/credentials.json"),'r'))

		self.twtapi = twitter.Api(consumer_key=credentials["Twitter API Key"],
							 consumer_secret=credentials["Twitter API Secret"],
							 access_token_key=credentials["Twitter Access Token"],
							 access_token_secret=credentials["Twitter Token Secret"]	
			)

	def post(self,media,msg):
		self.twtapi.PostUpdates(status=msg,media=media) 





def tests():
	bot = TwitBot()

	msg = "Pronóstico Numérico de la precipitación para las próximas 24 horas a partir del modelo WRF-SisPI (Inicializado el día 2020-10-14 12:00 UTC/Hora local: 2020-10-14 08:00 AM)"
	vidfile ="/home/miguel/Downloads/wrfout_2020101412_d3_rain_sfc_.mp4"

	bot.post(msg,vidfile)



if __name__ == '__main__':
	bot = TwitBot()
	tests()
