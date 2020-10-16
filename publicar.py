#!/usr/bin/env python

from CFABot import CFABot
import json
import sys
import time
import datetime 
import pytz
from glob import glob
from os.path import join, exists,expanduser
from scripts.imgconvert import pngs2mp4


def check_sended(corrida, log='msgbox.log'):
    with open(log, 'r') as f:
        msgs = f.readlines()
        if len(msgs) > 0:
            last_msg = msgs[-1].strip('\n')
            if last_msg == corrida:
                return True
    return False


def is_ready(outputdir,curoutput):
    """ Vigilar carpetas de gráficos para correr independiente de script de sispi"""

    if not exists(join(outputdir, curoutput, "wrfout_" + curoutput)):
        print("La última corrida no está lista")
        return 1

    #  RAIN
   
    count = 24

    if len(glob(lluviafiles +
                "*.png")) < count:  # espera la cantidad fijada de archivos
        print("Los últimos gráficos no están listos")
        return 1

    if check_sended(curoutput):
        print('Salidas ya enviadas anteriormente')
        return 1
    return 0    



def publicar():

    bot=CFABot()
    cycles = ['00', '06', '12', '18']

    
    nowgmt = time.gmtime()

    currcycle = cycles[int(nowgmt.tm_hour / 6)]  # ultima corrida
    
    initdateZ = datetime.datetime(nowgmt.tm_year,nowgmt.tm_mon,nowgmt.tm_mday,int(currcycle),0,tzinfo=pytz.UTC)
    initdateL = initdateZ.astimezone()


    outputdir = "/opt/sispi/OUTPUTS_1W/outputs"
    curoutput = initdateZ.strftime('%Y%m%d%H')


   
    #Rain

    lluviafiles = join(outputdir, curoutput, "wrfout_" + curoutput, 'SFC/RAIN',
                       "wrfout_" + curoutput + "_d3_rain_sfc_*")
    caption = """Pronóstico Numérico de la precipitación para las próximas 24 horas a partir del modelo WRF-SisPI (Inicializado el día {} UTC/Hora local: {}) """.format(
        initdateZ.strftime('%Y-%m-%d %H:%M',),initdateL.strftime('%Y-%m-%d %I:%M %p'))
    vidfile = pngs2mp4(lluviafiles, imagesize='480x320')
    
    # publicar
    bot.post_vid(caption,vidfile)




    open('msgbox.log', 'a').write(curoutput + '\n')


if __name__ == '__main__':
    publicar()
    #vidfile = '/home/miguel/Projects/cfabots/images/wrfout_2020082806/SFC/RAIN/wrfout_2020082806_d3_rain_sfc_.mp4'
    #bot = TelBot("1314850663:AAFuBzMDs5niJiUXHvH6ZaWI9rXHaz7GX8A")
    #bot.sendVideo(572031301, video=open(vidfile, 'rb'), width=480, height=320)
