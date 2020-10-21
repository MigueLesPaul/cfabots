#!/usr/bin/env python

import sys
from CFABot import CFABot
import json
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



def publicar(salida=None):
    """ 
    En caso de no especificar la salida publica la última que ya esté completa

    """

    bot=CFABot()
    outputdir = "/opt/sispi/OUTPUTS_1W/outputs"

    cycles = ['00', '06', '12', '18']
   
    currcycle = cycles[int(nowgmt.tm_hour / 6)]  # ultima corrida SisPI
        
    nowgmt = time.gmtime()
    initdateZ = datetime.datetime(nowgmt.tm_year,nowgmt.tm_mon,nowgmt.tm_mday,int(currcycle),0,tzinfo=pytz.UTC)
    initdateL = initdateZ.astimezone()


    if salida==None:
        curoutput = initdateZ.strftime('%Y%m%d%H')
    else:
        curoutput = salida

   
    #Rain

    lluviafiles = join(outputdir, curoutput, "wrfout_" + curoutput, 'SFC/RAIN',
                       "wrfout_" + curoutput + "_d3_rain_sfc_*")
    caption = """Pronóstico Numérico de la precipitación para las próximas 24 horas a partir del modelo WRF-SisPI (Inicializado el día {} UTC/Hora local: {}) """.format(
        initdateZ.strftime('%Y-%m-%d %H:%M',),initdateL.strftime('%Y-%m-%d %I:%M %p'))
    vidfile = pngs2mp4(lluviafiles, imagesize='480x320')
    
    # publicar
    bot.post_vid(caption,vidfile)




    open('msgbox.log', 'a').write(curoutput + '\n')


def publicaSisPI(salida):
    if len(salida)!=10:
        print("Error de entrada de fecha")
        sys.exit()

    bot=CFABot()
    outputdir = "/opt/sispi/OUTPUTS_1W/outputs"
    curoutput = salida

    initdateZ = datetime.datetime(int(salida[:4]),int(salida[4:6]),int(salida[6:8]),int(salida[8:10]),0,tzinfo=pytz.UTC)
    initdateL = initdateZ.astimezone()
   



    # RAIN

    lluviafiles = join(outputdir, curoutput, "wrfout_" + curoutput, 'SFC/RAIN',
                       "wrfout_" + curoutput + "_d3_rain_sfc_*")
    caption = """Pronóstico Numérico de la precipitación para las próximas 24 horas a partir del modelo WRF-SisPI (Inicializado el día {} UTC/Hora local: {}) """.format(
        initdateZ.strftime('%Y-%m-%d %H:%M',),initdateL.strftime('%Y-%m-%d %I:%M %p'))
    
    vidfile = pngs2mp4(lluviafiles, imagesize='480x320')
    bot.post_vid(caption,vidfile)
    print('publicado SisPI '+curoutput)
    open('msgbox.log', 'a').write(curoutput + '\n')
    sys.exit()




def publicaSPNOA(salida):
    if len(salida)!=10:
        print("Error de entrada de fecha")
        sys.exit()

    bot=CFABot()
    outputdir = "/opt/spnoa/OUTPUTS_1W/outputs"
    curoutput = salida

    initdateZ = datetime.datetime(int(salida[:4]),int(salida[4:6]),int(salida[6:8]),int(salida[8:10]),0,tzinfo=pytz.UTC)
    initdateL = initdateZ.astimezone()
   


    #WWW III

    oleaje = join(outputdir, curoutput, "ww3_" + curoutput+"0000", 'ww3_graphic_output',
                       "ww3_caribe_hs_sfc_[1,2,3]*")                                                # seleccionando las 24h a partir de las primeras 12

    caption = """Pronóstico Numérico de oleaje para las próximas 24h a partir del modelo WWIII-SPNOA (Inicializado el día {} UTC/Hora local: {}) """.format(
        initdateZ.strftime('%Y-%m-%d %H:%M',),initdateL.strftime('%Y-%m-%d %I:%M %p'))
    vidfile = pngs2mp4(oleaje, imagesize='480x320')
    bot.post_vid(caption,vidfile)
    print('publicado Spnoa WWIII'+curoutput)

    #SWAN

    oleaje = join(outputdir, curoutput, "ww3_" + curoutput+"0000", 'ww3_graphic_output',
                       "swan_cuba_hs_sfc_[1,2,3]*")                                                    # seleccionando las 24h a partir de las primeras 12

    caption = """Pronóstico Numérico de oleaje para las próximas 24h a partir del modelo SWAN-SPNOA(Inicializado el día {} UTC/Hora local: {}) """.format(
        initdateZ.strftime('%Y-%m-%d %H:%M',),initdateL.strftime('%Y-%m-%d %I:%M %p'))
    
    vidfile = pngs2mp4(oleaje, imagesize='480x320')
    bot.post_vid(caption,vidfile)
    print('publicado Spnoa SWAN'+curoutput)




if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Error. Faltan argumentos")
    else:
        if sys.argv[1] == 'sispi':
            publicaSisPI(sys.argv[2])
            sys.exit()
        elif sys.argv[1] == 'spnoa':
            publicaSPNOA(sys.argv[2])
    